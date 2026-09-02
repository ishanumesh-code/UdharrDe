from fastapi import APIRouter, HTTPException
from .schemas import (createExpense,createExpenseGrp)
from database.grp_data import (grpid_by_name)
from database.exp_data import (create_exp_user,get_user_exp, create_exp_grp)
from database.user_data import (get_user_by_name)

expenses = APIRouter(prefix="/expenses", tags=["expenses"])

@expenses.post("/create_expense")
def create_expense(expenseData: createExpense):
    '''needs name , payers uid, amount, and receiver uid to create an expensebetween them'''
    if not expenseData.name:
        raise HTTPException(status_code=400, detail="Expense name is required")
    if not expenseData.p_uid:
        raise HTTPException(status_code=400, detail="Payer user ID is required")
    if not expenseData.amt:
        raise HTTPException(status_code=400, detail="Amount is required")
    if not expenseData.u_uid:
        raise HTTPException(status_code=400, detail="Receiver user ID is required")
    
    create_exp_user(expenseData.name,expenseData.p_uid, expenseData.amt, expenseData.u_uid)
    raise HTTPException(status_code=200, detail=f"Expense '{expenseData.name}' created successfully")

@expenses.post("/get_user_expenses")
def get_user_expenses(uid: str):
    '''gives all the expenses of that user in a list of dictonaries'''
    if not uid:
        raise HTTPException(status_code=400, detail="User ID is required")
    
    expenses = get_user_exp(uid)
    return expenses

#exp_relation wala mujhe nhi samjha agar tujhe samjha toh kar de
#=================================================================================================================================
#=================================================================================================================================

@expenses.post("/create_expense_grp")
def create_expense_grp(expenseData: createExpenseGrp):
    '''needs name , payers name, amount, and group name to create an expense between them'''
    if not expenseData.name:
        raise HTTPException(status_code=400, detail="Expense name is required")
    if not expenseData.payerName:
        raise HTTPException(status_code=400, detail="Payer user ID is required")
    if not expenseData.amt:
        raise HTTPException(status_code=400, detail="Amount is required")
    if not expenseData.grpName:
        raise HTTPException(status_code=400, detail="Group name is required")
    
    g_uid = grpid_by_name(expenseData.grpName)
    if not g_uid:
        raise HTTPException(status_code=404, detail=f"Group '{expenseData.grpName}' not found")

    p_uid = get_user_by_name(expenseData.payerName)["id"]
    if not p_uid:
        raise HTTPException(status_code=404, detail=f"Payer '{expenseData.payerName}' not found")
    
    if len(expenseData.friends) != len(expenseData.money):
        raise HTTPException(status_code=400, detail="Length of names and money lists must be the same")
    
    split={}
    ids=[]
    for i in expenseData.friends:
        try:
            dataMembers = get_user_by_name(i)
            ids.append(dataMembers["id"])
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error retrieving user '{i}': {str(e)}")

    for i in range(len(expenseData.friends)):
        split[ids[i]]=expenseData.money[i]


    create_exp_grp(expenseData.name, p_uid, expenseData.amt, g_uid, split)
    raise HTTPException(status_code=200, detail=f"Expense '{expenseData.name}' created successfully for group '{expenseData.grpName}'")
from pydantic import BaseModel

class createExpense(BaseModel):
    name: str
    p_uid: str
    amt: float
    u_uid: str

class createExpenseGrp(BaseModel):
    name: str
    payerName: str
    amt: float
    grpName: str
    friends: list
    money: list[int]
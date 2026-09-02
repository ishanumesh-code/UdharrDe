from .client import supabase #.removed before client for local checking

def create_exp_user(name: str, p_uid: str, amt: float, u_uid: str, comment=None):
    '''public
    output: none
    it is used to create an expense between 2 users'''
    try:
        data={
            "name":name,
            "paid_by": p_uid,
            "amt": amt,
            "u_pay": u_uid,
            "g_pay": None,
            "split": {},
            "diff": 0,
            "comment": comment
        }
        supabase.table("expenses").insert(data).execute()
        # response1=supabase.table("users").
        exp_relation(p_uid, u_uid, amt)
        exp_relation(u_uid, p_uid, (-1)*amt)
        print(f"{name} expense added")
    except Exception as e:
        print(f"Error: {e}")
        raise e

def exp_relation(uid1: str, uid2: str, amt: float):
    '''public
    output:none
    this updates the amt data in user exp relation in users table
    Note: +amt means lended and - means owed money'''
    try:
        response=supabase.table("users").select("exp_frnd", "tot_owe", "tot_lend").eq("id", uid1).execute()
        if response:
            exp_dict=response.data[0]["exp_frnd"]
            owed=response.data[0]["tot_owe"]
            lended=response.data[0]["tot_lend"]
            if uid2 in exp_dict.keys():
                exp_dict[uid2]+=amt
            else:
                exp_dict[uid2]=amt
            if amt>0:
                lended+=amt
            else:
                owed-=amt
            supabase.table("users").update({"exp_frnd": exp_dict, "tot_owe": owed, "tot_lend": lended}).eq("id", uid1).execute()
            print("expense data updated")
        else:
            print("user doesn't exist")
    except Exception as e:
        print(f"Error: e")
        raise e

def create_exp_grp(name: str, p_uid: str, amt: float, g_uid: str, split: dict, comment=None):
    #split is a dict with the format {mem_uid(str): share(float)}
    #remember add only the uids of users who are already member of that group
    try:
        count=0
        for val in split.values():
            count+=val
        
        data={
            "name": name,
            "paid_by": p_uid,
            "amt": amt,
            "u_pay": None,
            "g_pay": g_uid,
            "split": split,
            "diff": amt-count,
            "comment": comment
        }
        supabase.table("expenses").insert(data).execute()
        print(f"{name} expense added")
    except Exception as e:
        print(f"Error: {e}")
        raise e

# def split_handle(uid_1: str, split: dict):
#     response=supabase.table("users").select("*").eq("id",uid_1).execute()
#     for key, val in split.items():


def get_user_exp(uid: str):
    '''public
    ouput: expenses of a user-> (list of dicts)
    when given a user uid it returns all expenses involving the user either in a payer section or receiver section or in grp split'''
    try:
        response=supabase.table("expenses").select("*").eq("paid_by", uid).or_(f"paid_by.eq.{uid}, u_pay.eq.{uid}").execute()
        return response.data
    except Exception as e:
        print(f"Error: {e}")
        raise e

def get_grp_exp(g_uid: str):
    '''public
    output: expenses of a group -> (list of dicts)
    returns all expenses where g_pay == g_uid'''
    try:
        response = supabase.table("expenses").select("*").eq("g_pay", g_uid).execute()
        return response.data or []
    except Exception as e:
        print(f"Error: {e}")
        raise e

def update_exp(uid: str, name=None, amt=None, split=None, comment= None):
    '''public
    ouput: none
    enter uid and updates u need in the expense
    remember as multiple none are there specify the input argument variable with value
    ex: update_exp("dbf9296e-4284-4de6-8956-b4ddd1f2f3ce", amt=5000, comment= "kyu bolti public", split= {"6c1363ba-ae17-43e4-82e2-89894e651e89": 4500, "b7ca1ba3-3bf6-4e82-849b-a4ac44b6ac62": 480})'''
    try:
        response=supabase.table("expenses").select("*").eq("id", uid).execute()
        if not name:
            name = response.data[0]["name"]
        if not amt:
            amt = response.data[0]["amt"]
        if not split:
            split = response.data[0]["split"]
        if not comment:
            comment = response.data[0]["comment"]
        if split.items():
            count=0
            for val in split.values():
                count+=val
            diff= amt-count
        else:
            diff=0
        
        supabase.table("expenses").update({"name": name, "amt": amt, "split": split, "comment": comment, "diff": diff}).eq("id", uid).execute()
        print(f"{name} expense updated")
    except Exception as e:
        print(f"Error: {e}")
        raise e


# create_exp_user("exp2", "6c1363ba-ae17-43e4-82e2-89894e651e89", 100, "7c1363ba-ae17-43e4-82e2-89894e651e89", "world world")
# create_exp_grp("njc_chacha", "6c1363ba-ae17-43e4-82e2-89894e651e89", 2500, "c365fece-daa1-4100-9c68-0a7115b597b0", {"6c1363ba-ae17-43e4-82e2-89894e651e89": 1500, "b7ca1ba3-3bf6-4e82-849b-a4ac44b6ac62": 990})
# create_exp_user("tech", "564bc79e-705f-440a-8adc-48787d37ab79", 430, "6c1363ba-ae17-43e4-82e2-89894e651e89")
# print(get_user_exp("6c1363ba-ae17-43e4-82e2-89894e651e89"))
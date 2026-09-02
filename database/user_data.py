from datetime import datetime
from .client import supabase #.removed before client for local checking

#USERS

def create_user(user_uid: str, name: str, phone: str, mail: str):
    '''private(auth will use it)
    output: user uid
    call after authentification so user is created in public.user'''
    now = datetime.now().strftime("%b-%d-%Y %H:%M:%S")

    try:
        user_data={
            "id": user_uid,
            "name": name,
            "phone": phone,
            "friends": [],
            "in_grp": [],
            "exp_frnd": {},
            "tot_owe": 0,
            "tot_lend": 0,
            "created_at": now,
            "email": mail
        }
        response= supabase.table("users").insert(user_data).execute()
        print("user created successfully")
        return user_uid
    except Exception as e:
        print(f"Error: {e}")
        raise e

def update_user(uid: str, new_name=False, new_phone=False):
    '''public
    output: none
    uses uid to get user info and update name or phone whichever is given'''
    try:
        response = supabase.table("users").select("*").eq("id", uid).execute()
        if not response.data or len(response.data) == 0:
            print("User not found for update")
            return
        curr_data = response.data[0]
        if not new_name:
            new_name = curr_data["name"]
        if not new_phone:
            new_phone = curr_data["phone"]
        supabase.table("users").update({"name": new_name, "phone": new_phone}).eq("id", uid).execute()
        print("user data updated")
    except Exception as e:
        print(f"Error: {e}")
        raise e

def get_user_by_id(uid: str):
    '''private (fast api side may use it)
    output: user data->(dict)
    using user uid it returns its whole data'''
    try:
        response = supabase.table("users").select("*").eq("id", uid).execute()
        if response.data:
            return response.data[0]
        else:
            print(f"user not found")
    except Exception as e:
        print(f"Error fetching user by id {uid}: {e}")
        return None

def get_user_by_id_list(list_uid: list)-> list:
    '''private (fast api may use it, summi uses it rn)
    output: id and name of users passed in the arg ->(list of dicts)
    using user uids it returns the dict of ids and names'''
    try:
        response=supabase.table("users").select("id", "name").in_("id", list_uid).execute()
        if response.data:
            return response.data
        else:
            print(f"users not found")
    except Exception as e:
        print(f"Error: {e}")
        raise e

def get_user_by_name(name: str):
    '''public & private
    output: whole data of user ->(dict)
    using user name it returns the whole user data'''
    try:
        response= supabase.table("users").select("*").eq("name", name).execute()
        if not response.data:
            return ("User doesn't exist")
        return response.data[0]
    except Exception as e:
        print(f"Error: {e}")
        raise e

def get_user_by_mail(mail: str):
    '''public
    output: whole data of user ->(dict)
    using user email gives the whole data of user'''
    try:
        response= supabase.table("users").select("*").eq("email", mail).execute()
        if not response.data:
            return ("User doesn't exist")
        return response.data[0]
    except Exception as e:
        print(f"Error: {e}")
        raise e

def is_friend(uid1: str, uid2: str) ->bool:
    '''public and private(need to show if a user is ones friend when searched too)
    output: true if friends else false ->(bool)
    using uids of both friends tells if they are friends'''
    response=(supabase.table("users").select("friends").eq("id",uid1).execute())
    friends=response.data[0]["friends"]
    if uid2 in friends:
        return True
    else:
        return False

def add_f_helper(uid1: str, uid2: str):
    '''private(for database)
    output: none
    helper function to help add friends list of users table'''
    response=(supabase.table("users").select("friends").eq("id",uid1).execute())
    friends=response.data[0]["friends"]
    if not is_friend(uid1, uid2):
        friends.append(uid2)
        supabase.table("users").update({"friends": friends}).eq("id", uid1).execute()
        print("friend added")
    else:
        print("friend already exists")

def rm_f_helper(uid1: str, uid2: str):
    '''private(database uses it)
    output: none
    helper function to help rm user from friends list in users table'''
    response=(supabase.table("users").select("friends").eq("id",uid1).execute())
    friends=response.data[0]["friends"]
    if is_friend(uid1, uid2):
        friends.remove(uid2)
        supabase.table("users").update({"friends": friends}).eq("id", uid1).execute()
        print("friend removed")
    else:
        print("not friends")

def add_friends(uid1: str, uid2: str):
    '''public
    output: none
    it adds friends mutually'''
    try:
        add_f_helper(uid1, uid2)
        add_f_helper(uid2, uid1)
    except Exception as e:
        print(f"Error: e")
        raise e

def rm_friends(uid1, uid2):
    '''public
    ouput: none
    it removes friends from  each others list mutually'''
    try:
        rm_f_helper(uid1, uid2)
        rm_f_helper(uid2, uid1)
    except Exception as e:
        print(f"Error: e")
        raise e

def get_user_grps(uid: str)-> list:
    '''public
    output: list of uuids of grps a user is in
    use uid of user to return the list of grp ids of grps in which the user is a member of'''
    try:
        response=supabase.table("users").select("in_grp").eq("id", uid).execute()
        if response.data:
            return response.data[0]["in_grp"]
        else:
            print(f"user doesn't exist")
    except Exception as e:
        print(f"Error: {e}")
        raise e

def get_user_frnds(uid: str):
    '''public
    output: list of friend uids-> (list of uids)
    give uid of user and get his friend list'''
    try:
        response=supabase.table("users").select("friends").eq("id", uid).execute()
        if response:
            return response.data[0]["friends"]
        else:
            print(f"user doesn't exist")
    except Exception as e:
        print(f"Error {e}")
        raise e

def get_exp_frnds(uid: str):
    '''public
    ouput: {uid: exp}-> (dict)
    output will give a dict with friend uid as key and exp with the user as value'''
    try:
        response=supabase.table("users").select("exp_frnd").eq("id", uid).execute()
        if response:
            return response.data[0]["exp_frnd"]
        else:
            print("user doesn't exist")
    except Exception as e:
        print(f"Error: e")
        raise e
#-------------------
# create_user
# create_user("6c1363ba-ae17-43e4-82e2-89894e651e89", "asdf", '9876543210', "mail@mail.com")
# update_user
# update_user("6c1363ba-ae17-43e4-82e2-89894e651e89", "qwerdf", '5432109876')
#add_friends
# add_friends("6c1363ba-ae17-43e4-82e2-89894e651e89", "7c1363ba-ae17-43e4-82e2-89894e651e89")
# print(get_user_by_id("6c1363ba-ae17-43e4-82e2-89894e651e89"))
# print("------------------")
# print(get_user_by_name("asdf"))
# print("------------------")
# print(get_user_by_mail("mail@mail.com"))
# print(is_friend("6c1363ba-ae17-43e4-82e2-89894e651e89", "7c1363ba-ae17-43e4-82e2-89894e651e89"))
# rm_friends("7c1363ba-ae17-43e4-82e2-89894e651e89", "6c1363ba-ae17-43e4-82e2-89894e651e89")
# rm_friends("6c1363ba-ae17-43e4-82e2-89894e651e89", "7c1363ba-ae17-43e4-82e2-89894e651e89")
# hello=(get_user_grps("6c1363ba-ae17-43e4-82e2-89894e651e89"))
# print(grp_info_by_id(hello[0]))
# print(get_user_by_id_list(["564bc79e-705f-440a-8adc-48787d37ab79", "6c1363ba-ae17-43e4-82e2-89894e651e89"]))
#print(get_user_frnds("7c1363ba-ae17-43e4-82e2-89894e651e89"))
# print(get_user_by_id_list(["564bc79e-705f-440a-8adc-48787d37ab79", "6c1363ba-ae17-43e4-82e2-89894e651e89"]))

from .client import supabase #.removed before client for local checking
from datetime import datetime

#GROUPS
def create_grp(name: str, creator_uid: str):
    '''public
    output: none
    it creates a group once name is given
    gets the creator uid from the tokens from frontend and then adds the creator as the first member'''
    try:
        response=supabase.table("groups").select("name").execute()
        name_list=response.data["name"]
        if(name not in name_list):
            grp_data={
                "name": name,
                "created_by": creator_uid,
                "members": []
            }
            supabase.table("groups").insert(grp_data).execute()
            print("group created")
            add_mem(name, [str(creator_uid)])
        else:
            print(f"a group by name {name} already exists. Please choose another name")
    except Exception as e:
        print(f"Error: {e}")
        raise e

def grpid_by_name(name: str)-> str:
    '''private (fast api might use it to get id of group from name)
    output: grp id-> (str)
    gives the '''
    try:
        response=supabase.table("groups").select("*").eq("name", name).execute()
        if response.data:
            return response.data[0]["id"]
        else:
            print(f"no grp by name {name} exists")
    except Exception as e:
        print(f"Error: {e}")
        raise e

def grp_info_by_id(gid):
    '''get all grp info using grp id
    if u don't have grp id and have grp name then use grpid_by_name(name) and get the id and then call this function'''
    try:
        response=supabase.table("groups").select("*").eq("id", gid).execute()
        if response.data:
            return response.data[0]
        else:
            print(f"no group exists by id {gid}")
    except Exception as e:
        print(f"Error: {e}")
        raise e

def get_grp_by_id_list(list_uid: list)-> dict:
    '''private (fast api may use it, summi uses it rn)
    output: id and name of grps passed in the arg ->(list of dicts)
    using grp uids it returns the dict of ids and names'''
    try:
        response=supabase.table("groups").select("id", "name").in_("id", list_uid).execute()
        if response.data:
            return response.data
        else:
            print(f"groups don't exist")
    except Exception as e:
        print(f"Error: {e}")
        raise e

def add_in_grp(uid: str, grp_id: str):
    '''private
    output: none
    adds grps in in_grp column of users'''
    try:
        response=supabase.table("users").select("in_grp").eq("id", uid).execute()
        grp_list=response.data[0]["in_grp"]
        if(grp_id not in grp_list):
            grp_list.append(grp_id)
            supabase.table("users").update({"in_grp": grp_list}).eq("id", uid).execute()
            print(f"{grp_id} added in user {uid}")
        else:
            print(f"{grp_id} already in user {uid} list")
    except Exception as e:
        print(f"Error: {e}")
        raise e

def rm_in_grp(uid: str, grp_id: str):
    '''private
    output: none
    removes grps in in_grp of users'''
    try:
        response=supabase.table("users").select("in_grp").eq("id", uid).execute()
        grp_list=response.data[0]["in_grp"]
        if(grp_id in grp_list):
            grp_list.remove(grp_id)
            supabase.table("users").update({"in_grp": grp_list}).eq("id", uid).execute()
            print(f"{grp_id} rm from user {uid}")
        else:
            print(f"{grp_id} doesn't exist in user {uid} list")
    except Exception as e:
        print(f"Error: e")
        raise e

def add_mem(grp_id: str, arr_name: list):
    '''note the parameter of grp_name is changed with grp_id @fast_api
    public
    output: none
    adds members in a group'''
    try:
        response=supabase.table("groups").select("members", "id").eq("id", grp_id).execute()
        mem_list=response.data[0]["members"]
        for items in arr_name:
            add_in_grp(str(items), grp_id)
            if items not in mem_list:
                mem_list.append(items)
                print(f"{items} added")
            else:
                print(f"{items} already in grp")
        supabase.table("groups").update({"members": mem_list}).eq("id", grp_id).execute()
        print(f"users added {arr_name} in grp {grp_id}")
    except Exception as e:
        print(f"Error: {e}")
        raise e

def rm_member(grp_id: str, arr_name: list):
    try:
        response=supabase.table("groups").select("members", "id").eq("id", grp_id).execute()
        mem_list=response.data[0]["members"]
        for items in arr_name:
            rm_in_grp(str(items), grp_id)
            if items in mem_list:
                mem_list.remove(items)
                print(f"user {items} removed from grp {grp_id}")
            else:
                print(f"{items} already in grp")
        # rm_in_grp(uid, grp_id)
        # if(uid in mem_list):
        #     mem_list.remove(uid)
        #     print(f"user {uid} removed from grp {grp_name}")
        # else:
        #     print(f"user {uid} not in grp {grp_name}")
        supabase.table("groups").update({"members": mem_list}).eq("id", grp_id).execute()
        print(f"user {arr_name} removed from grp {grp_id}")
    except Exception as e:
        print(f"Error: {e}")
        raise e
    



#---------------------------------------------------------------------
# create_grp("group1", "6c1363ba-ae17-43e4-82e2-89894e651e89")
# print(grpid_by_name("group1"))
# add_mem("group1", ["7c1363ba-ae17-43e4-82e2-89894e651e89"])
# rm_member("group1", "7c1363ba-ae17-43e4-82e2-89894e651e89")
# rm_member("testing grp", ["6c1363ba-ae17-43e4-82e2-89894e651e89"])
# print(grpid_by_name("hello hello hello"))
# print(grp_info_by_id("3fef5e88-8fae-44df-ab49-3b77409eb5d1"))
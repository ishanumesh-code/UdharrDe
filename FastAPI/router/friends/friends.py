from fastapi import FastAPI, APIRouter , HTTPException
from .schemas import create_Remove_Friend
from database.user_data import ( get_user_by_name,  get_user_by_mail, add_friends, rm_friends)

friends= APIRouter(prefix="/friends", tags=["friends"])

@friends.post("/add")
def addFriend(friendData: create_Remove_Friend):
    if not friendData.friend_name and not friendData.friend_email:
        raise HTTPException(status_code=400, detail="Friend ID is required")
    if not friendData.user_uid:
        raise HTTPException(status_code=400, detail="User ID is required")
    try :
        if friendData.friend_name != None:
            friend_data = get_user_by_name(friendData.friend_name)
        else:
            friend_data = get_user_by_mail(friendData.friend_email)
        if not friend_data:
            raise HTTPException(status_code=404,detail="Friend doesn't exist")
        friend_uid = friend_data["id"]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error retrieving friend: {str(e)}")

    if str(friendData.user_uid) == str(friend_uid):
        raise HTTPException(status_code=400, detail="Cannot add yourself as a friend")

    try:
        add_friends(str(friendData.user_uid), str(friend_uid))
        return {"message": "Friend added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding friend: {str(e)}")


@friends.post("/remove")
def removeFriend(friendData: create_Remove_Friend): 
    if not friendData.friend_name and not friendData.friend_email:
        raise HTTPException(status_code=400, detail="Friend ID is required")
    if not friendData.user_uid:
        raise HTTPException(status_code=400, detail="User ID is required")
    try :
        if friendData.friend_name != None:
            friend_data = get_user_by_name(friendData.friend_name)
        else:
            friend_data = get_user_by_mail(friendData.friend_email)
        if not friend_data:
            raise HTTPException(status_code=404,detail="Friend not found")
        friend_uid = friend_data["id"]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error retrieving friend: {str(e)}")

    if str(friendData.user_uid) == str(friend_uid):
        raise HTTPException(status_code=400, detail="Cannot remove yourself as a friend")

    try:
        rm_friends(str(friendData.user_uid), str(friend_uid))
        return {"message": "Friend removed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error removing friend: {str(e)}")
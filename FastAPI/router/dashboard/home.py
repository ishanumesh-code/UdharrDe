from fastapi import APIRouter, Depends, HTTPException
from database.user_data import get_user_by_id, update_user, get_users_from_ids
from database.grp_data import get_group_by_id, get_groupnames_from_ids
from router.auth.deps import get_current_user
from router.auth.schemas import UserResponse
from .schemas import DashboardResponse, UpdateProfileRequest, GroupResponse
import uuid
import logging
logger = logging.getLogger(__name__)

home = APIRouter(prefix="/dashboard", tags=["dashboard"])

def format_user_dashboard(user: dict) -> dict:
    friends_list = user.get("friends") or []
    groups_list = user.get("in_grp") or []
    exp_dict = user.get("exp_frnd") or {}

    user_map = get_users_from_ids(friends_list + list(exp_dict.keys()))
    group_map = get_groupnames_from_ids(groups_list)

    user_copy = dict(user)
    user_copy["friends"] = [{"id": f, "name": user_map.get(str(f), "User")} for f in friends_list]
    user_copy["in_grp"] = [{"id": g, "name": group_map.get(str(g), "Group")} for g in groups_list]
    user_copy["exp_frnd"] = [{"id": f, "name": user_map.get(str(f), "User"), "amount": amt} for f, amt in exp_dict.items()]

    return user_copy

@home.get("/", response_model=DashboardResponse)
def dashboard(current_user: UserResponse = Depends(get_current_user)):
    user = get_user_by_id(current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return DashboardResponse(**format_user_dashboard(user))

@home.put("/update", response_model=DashboardResponse)
def update_profile(update_paras: UpdateProfileRequest, current_user: UserResponse = Depends(get_current_user)):
    user = get_user_by_id(current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_user(current_user.id, update_paras.display_name, update_paras.phone)
    updated_user = get_user_by_id(current_user.id)
    return DashboardResponse(**format_user_dashboard(updated_user))

@home.get("/friend/{id}", response_model=DashboardResponse)
def get_friend_transactions(id: uuid.UUID, current_user: UserResponse = Depends(get_current_user)):
    user = get_user_by_id(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return DashboardResponse(**format_user_dashboard(user))

@home.get("/groups/{id}", response_model=GroupResponse)
def get_group_transactions(id: uuid.UUID, current_user: UserResponse = Depends(get_current_user)):
    group = get_group_by_id(id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    members_list = group.get("members") or []
    created_by_id = str(group.get("created_by") or "")
    
    user_map = get_users_from_ids(members_list + ([created_by_id] if created_by_id else []))
    
    group_copy = dict(group)
    group_copy["members"] = [{"id": m, "name": user_map.get(str(m), "User")} for m in members_list]
    group_copy["created_by_name"] = user_map.get(created_by_id, "User")
    
    return GroupResponse(**group_copy)
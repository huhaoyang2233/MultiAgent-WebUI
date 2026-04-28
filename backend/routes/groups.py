from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from data.database import JSONDatabase
import uuid
from datetime import datetime
from routes.auth import get_current_user

router = APIRouter(prefix="/groups", tags=["群聊"])

db = JSONDatabase("groups")
sessions_db = JSONDatabase("sessions")

class Group(BaseModel):
    id: str
    name: str
    avatar: str
    member_count: int
    unread: int
    members: list
    created_at: str

class GroupCreate(BaseModel):
    name: str
    avatar: str
    members: list

@router.get("/", summary="获取当前用户的群聊列表")
async def get_groups(current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    groups_data = db.get(user_id, [])
    return {"groups": groups_data}

@router.get("/{group_id}", response_model=Group, summary="获取单个群聊")
async def get_group(group_id: str, current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    groups_data = db.get(user_id, [])
    group = next((g for g in groups_data if g["id"] == group_id), None)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

@router.post("/", response_model=Group, summary="创建群聊")
async def create_group(group: GroupCreate, current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    groups_data = db.get(user_id, [])
    
    if any(g["name"] == group.name for g in groups_data):
        raise HTTPException(status_code=400, detail="Group name already exists")
    
    new_group = {
        "id": f"group-{uuid.uuid4().hex[:8]}",
        "name": group.name,
        "avatar": group.avatar,
        "member_count": len(group.members),
        "unread": 0,
        "members": group.members,
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    
    groups_data.append(new_group)
    db.set(user_id, groups_data)
    
    return new_group

@router.put("/{group_id}/members", summary="添加群成员")
async def add_member(group_id: str, member_id: str, current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    groups_data = db.get(user_id, [])
    
    group_index = next((i for i, g in enumerate(groups_data) if g["id"] == group_id), -1)
    if group_index == -1:
        raise HTTPException(status_code=404, detail="Group not found")
    
    group = groups_data[group_index]
    
    if member_id in group["members"]:
        raise HTTPException(status_code=400, detail="Member already in group")
    
    group["members"].append(member_id)
    group["member_count"] = len(group["members"])
    db.set(user_id, groups_data)
    
    return {"message": "Member added successfully"}

@router.delete("/{group_id}/members", summary="移除群成员")
async def remove_member(group_id: str, member_id: str, current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    groups_data = db.get(user_id, [])
    
    group_index = next((i for i, g in enumerate(groups_data) if g["id"] == group_id), -1)
    if group_index == -1:
        raise HTTPException(status_code=404, detail="Group not found")
    
    group = groups_data[group_index]
    
    if member_id not in group["members"]:
        raise HTTPException(status_code=400, detail="Member not in group")
    
    group["members"].remove(member_id)
    group["member_count"] = len(group["members"])
    db.set(user_id, groups_data)
    
    return {"message": "Member removed successfully"}

@router.put("/{group_id}/unread", summary="更新未读消息数")
async def update_unread(group_id: str, unread: int, current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    groups_data = db.get(user_id, [])
    
    group_index = next((i for i, g in enumerate(groups_data) if g["id"] == group_id), -1)
    if group_index == -1:
        raise HTTPException(status_code=404, detail="Group not found")
    
    groups_data[group_index]["unread"] = unread
    db.set(user_id, groups_data)
    
    return {"message": "Unread count updated successfully"}

@router.delete("/{group_id}", summary="删除群聊")
async def delete_group(group_id: str, current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    groups_data = db.get(user_id, [])
    
    group_index = next((i for i, g in enumerate(groups_data) if g["id"] == group_id), -1)
    if group_index == -1:
        raise HTTPException(status_code=404, detail="Group not found")
    
    groups_data.pop(group_index)
    db.set(user_id, groups_data)
    
    return {"message": "Group deleted successfully"}
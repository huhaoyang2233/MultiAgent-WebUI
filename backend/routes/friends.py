from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from data.database import JSONDatabase
import uuid
from datetime import datetime
from routes.auth import get_current_user

router = APIRouter(prefix="/friends", tags=["好友"])

db = JSONDatabase("friends")

class Friend(BaseModel):
    id: str
    name: str
    avatar: str
    type: str
    role_id: str | None = None
    status: str
    created_at: str

class FriendCreate(BaseModel):
    name: str
    avatar: str
    type: str
    role_id: str | None = None

@router.get("/", summary="获取当前用户的好友列表")
async def get_friends(current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    friends_data = db.get(user_id, [])
    return {"friends": friends_data}

@router.get("/{friend_id}", response_model=Friend, summary="获取单个好友")
async def get_friend(friend_id: str, current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    friends_data = db.get(user_id, [])
    friend = next((f for f in friends_data if f["id"] == friend_id), None)
    if not friend:
        raise HTTPException(status_code=404, detail="Friend not found")
    return friend

@router.post("/", response_model=Friend, summary="添加好友")
async def add_friend(friend: FriendCreate, current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    friends_data = db.get(user_id, [])
    
    if any(f["name"] == friend.name for f in friends_data):
        raise HTTPException(status_code=400, detail="Friend already exists")
    
    new_friend = {
        "id": f"friend-{uuid.uuid4().hex[:8]}",
        "name": friend.name,
        "avatar": friend.avatar,
        "type": friend.type,
        "role_id": friend.role_id,
        "status": "online" if friend.type == "ai" else "offline",
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    
    friends_data.append(new_friend)
    db.set(user_id, friends_data)
    return new_friend

@router.put("/{friend_id}/status", summary="更新好友状态")
async def update_friend_status(friend_id: str, status: str, current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    friends_data = db.get(user_id, [])
    
    friend_index = next((i for i, f in enumerate(friends_data) if f["id"] == friend_id), -1)
    if friend_index == -1:
        raise HTTPException(status_code=404, detail="Friend not found")
    
    friends_data[friend_index]["status"] = status
    db.set(user_id, friends_data)
    
    return {"message": "Status updated successfully"}

@router.delete("/{friend_id}", summary="删除好友")
async def delete_friend(friend_id: str, current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    friends_data = db.get(user_id, [])
    
    friend_index = next((i for i, f in enumerate(friends_data) if f["id"] == friend_id), -1)
    if friend_index == -1:
        raise HTTPException(status_code=404, detail="Friend not found")
    
    friends_data.pop(friend_index)
    db.set(user_id, friends_data)
    
    return {"message": "Friend deleted successfully"}
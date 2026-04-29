from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from datetime import datetime
import uuid
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.database import JSONDatabase
from routes.auth import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])

users_db = JSONDatabase("users")
friends_db = JSONDatabase("friends")
groups_db = JSONDatabase("groups")

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str = "user"

class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None
    role: str | None = None

@router.get("/users", summary="获取所有用户列表")
async def get_users(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Permission denied")
    
    users = users_db.get("users", [])
    return users

@router.post("/users", summary="创建新用户")
async def create_user(user: UserCreate, current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Permission denied")
    
    users = users_db.get("users", [])
    
    if any(u["username"] == user.username for u in users):
        raise HTTPException(status_code=400, detail="Username already exists")
    
    if any(u["email"] == user.email for u in users):
        raise HTTPException(status_code=400, detail="Email already exists")
    
    new_user = {
        "id": f"user-{uuid.uuid4().hex[:8]}",
        "username": user.username,
        "password": user.password,
        "email": user.email,
        "avatar": f"https://i.pravatar.cc/40?img={len(users) + 1}",
        "role": user.role,
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    
    users.append(new_user)
    users_db.set("users", users)
    return new_user

@router.put("/users/{user_id}", summary="更新用户信息")
async def update_user(user_id: str, user_data: UserUpdate, current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Permission denied")
    
    users = users_db.get("users", [])
    index = next((i for i, u in enumerate(users) if u["id"] == user_id), -1)
    
    if index == -1:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_data.username and any(u["username"] == user_data.username and u["id"] != user_id for u in users):
        raise HTTPException(status_code=400, detail="Username already exists")
    
    if user_data.email and any(u["email"] == user_data.email and u["id"] != user_id for u in users):
        raise HTTPException(status_code=400, detail="Email already exists")
    
    update_data = user_data.dict(exclude_unset=True)
    users[index] = {**users[index], **update_data}
    users_db.set("users", users)
    return users[index]

@router.delete("/users/{user_id}", summary="删除用户")
async def delete_user(user_id: str, current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Permission denied")
    
    users = users_db.get("users", [])
    index = next((i for i, u in enumerate(users) if u["id"] == user_id), -1)
    
    if index == -1:
        raise HTTPException(status_code=404, detail="User not found")
    
    if users[index]["role"] == "admin":
        raise HTTPException(status_code=400, detail="Cannot delete admin user")
    
    deleted_user = users.pop(index)
    users_db.set("users", users)
    
    sessions_db = JSONDatabase("sessions.json")
    sessions_db.delete(user_id)
    
    sessions_dir = os.path.join(os.path.dirname(__file__), "..", "data", "sessions")
    if os.path.exists(sessions_dir):
        for filename in os.listdir(sessions_dir):
            if filename.startswith(f"{user_id}_"):
                os.remove(os.path.join(sessions_dir, filename))
    
    return {"message": "User deleted successfully", "user": deleted_user}

@router.get("/sessions", summary="获取所有用户的会话列表")
async def get_all_sessions(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Permission denied")
    
    sessions_db = JSONDatabase("sessions.json")
    all_sessions = sessions_db.get_all()
    
    result = {}
    sessions_dir = os.path.join(os.path.dirname(__file__), "..", "data", "sessions")
    
    for user_id, session_ids in all_sessions.items():
        if user_id == "_meta":
            continue
        
        user_sessions = []
        for session_id in session_ids:
            session_file = os.path.join(sessions_dir, f"{session_id}.json")
            message_count = 0
            
            if os.path.exists(session_file):
                import json
                with open(session_file, "r") as f:
                    try:
                        data = json.load(f)
                        message_count = len(data.get("messages", []))
                    except:
                        pass
            
            chat_type = "unknown"
            if session_id.startswith(f"{user_id}_agent_"):
                chat_type = "agent"
            elif session_id.startswith(f"{user_id}_friend_"):
                chat_type = "friend"
            elif session_id.startswith(f"{user_id}_group_"):
                chat_type = "group"
            
            user_sessions.append({
                "session_id": session_id,
                "chat_type": chat_type,
                "message_count": message_count
            })
        
        result[user_id] = user_sessions
    
    return result

@router.delete("/sessions/{session_id}", summary="删除会话")
async def delete_session(session_id: str, current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Permission denied")
    
    sessions_db = JSONDatabase("sessions.json")
    all_sessions = sessions_db.get_all()
    
    user_id = None
    for uid, session_ids in all_sessions.items():
        if session_id in session_ids:
            user_id = uid
            break
    
    if user_id is None:
        raise HTTPException(status_code=404, detail="Session not found")
    
    user_sessions = all_sessions[user_id]
    user_sessions.remove(session_id)
    sessions_db.set(user_id, user_sessions)
    
    sessions_dir = os.path.join(os.path.dirname(__file__), "..", "data", "sessions")
    session_file = os.path.join(sessions_dir, f"{session_id}.json")
    if os.path.exists(session_file):
        os.remove(session_file)
    
    return {"message": "Session deleted successfully"}

@router.get("/users/{user_id}/friends", summary="获取指定用户的好友列表")
async def get_user_friends(user_id: str, current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Permission denied")
    
    user_friends = friends_db.get(user_id, [])
    all_users = users_db.get("users", [])
    user_map = {u["id"]: u for u in all_users}
    
    friends_with_details = []
    for friend in user_friends:
        if friend.get("type") == "user" and friend.get("role_id"):
            user_info = user_map.get(friend["role_id"])
            if user_info:
                friend["username"] = user_info["username"]
                friend["email"] = user_info.get("email", "")
        friends_with_details.append(friend)
    
    return {"friends": friends_with_details}

@router.get("/users/{user_id}/groups", summary="获取指定用户的群组列表")
async def get_user_groups(user_id: str, current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Permission denied")
    
    all_groups = groups_db.get("groups", [])
    user_groups = []
    
    for group in all_groups:
        members = group.get("members", [])
        if user_id in members:
            user_groups.append(group)
    
    return {"groups": user_groups}
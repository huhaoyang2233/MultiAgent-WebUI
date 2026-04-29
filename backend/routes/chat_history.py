from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from data.session_database import SessionDatabase
import uuid
from datetime import datetime
from routes.auth import get_current_user

router = APIRouter(prefix="/chat-history", tags=["聊天记录"])

class Message(BaseModel):
    id: str
    role: str
    name: str
    content: str
    timestamp: str

class MessageCreate(BaseModel):
    role: str
    name: str
    content: str

def generate_session_id(user_id: str, target_id: str, target_type: str) -> str:
    return f"{user_id}_{target_type}_{target_id}"

@router.get("/", summary="获取用户所有聊天记录")
async def get_chat_history(current_user: dict = Depends(get_current_user)):
    user_sessions = SessionDatabase.get_user_sessions(current_user["id"])
    return {"chat_history": user_sessions}

@router.get("/{target_id}/{target_type}", summary="获取指定聊天记录")
async def get_chat(target_id: str, target_type: str, current_user: dict = Depends(get_current_user)):
    session_id = generate_session_id(current_user["id"], target_id, target_type)
    session_data = SessionDatabase.load_session(session_id)
    
    chat_data = {
        "id": session_id,
        "user_id": current_user["id"],
        "target_id": target_id,
        "target_type": target_type,
        "messages": session_data["messages"],
        "created_at": session_data["created_at"],
        "updated_at": session_data["updated_at"]
    }
    
    return {"chat": chat_data}

@router.post("/{target_id}/{target_type}/messages", summary="发送消息")
async def send_message(target_id: str, target_type: str, message: MessageCreate, current_user: dict = Depends(get_current_user)):
    session_id = generate_session_id(current_user["id"], target_id, target_type)
    
    new_message = {
        "id": f"msg-{uuid.uuid4().hex[:8]}",
        "role": message.role,
        "name": message.name,
        "content": message.content,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    SessionDatabase.add_message(session_id, new_message)
    return {"message": new_message}

@router.delete("/{target_id}/{target_type}", summary="清空聊天记录")
async def clear_chat(target_id: str, target_type: str, current_user: dict = Depends(get_current_user)):
    session_id = generate_session_id(current_user["id"], target_id, target_type)
    SessionDatabase.clear_messages(session_id)
    return {"message": "Chat history cleared successfully"}

@router.delete("/{target_id}/{target_type}/messages/{message_id}", summary="删除单条消息")
async def delete_message(target_id: str, target_type: str, message_id: str, current_user: dict = Depends(get_current_user)):
    session_id = generate_session_id(current_user["id"], target_id, target_type)
    success = SessionDatabase.delete_message(session_id, message_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Message not found")
    
    return {"message": "Message deleted successfully"}

@router.delete("/{target_id}/{target_type}/session", summary="删除整个会话")
async def delete_session(target_id: str, target_type: str, current_user: dict = Depends(get_current_user)):
    session_id = generate_session_id(current_user["id"], target_id, target_type)
    SessionDatabase.delete_session(session_id)
    return {"message": "Session deleted successfully"}

@router.get("/sessions/list", summary="获取用户所有会话列表")
async def list_sessions(current_user: dict = Depends(get_current_user)):
    sessions = SessionDatabase.get_user_sessions(current_user["id"])
    session_list = []
    for session in sessions:
        session_info = {
            "session_id": session["session_id"],
            "created_at": session["created_at"],
            "updated_at": session["updated_at"],
            "message_count": len(session.get("messages", []))
        }
        session_list.append(session_info)
    return {"sessions": session_list}

@router.get("/session/{session_id}", summary="通过session_id获取聊天历史")
async def get_session_history(session_id: str, current_user: dict = Depends(get_current_user)):
    session_data = SessionDatabase.load_session(session_id)
    
    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found")
    
    chat_data = {
        "id": session_id,
        "messages": session_data["messages"],
        "created_at": session_data["created_at"],
        "updated_at": session_data["updated_at"]
    }
    
    return {"chat": chat_data}
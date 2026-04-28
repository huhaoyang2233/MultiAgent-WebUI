from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from data.database import JSONDatabase
from data.session_database import SessionDatabase
from routes.auth import get_current_user
from datetime import datetime
import uuid

router = APIRouter(prefix="/chat", tags=["聊天"])

class ChatMessage(BaseModel):
    role: str
    name: str
    content: str

class ChatRequest(BaseModel):
    user_config: dict
    user_message: dict

ai_roles_db = JSONDatabase("ai_roles")
friends_db = JSONDatabase("friends")
groups_db = JSONDatabase("groups")
sessions_db = JSONDatabase("sessions")

AI_RESPONSES = {
    "role-1": [
        "根据当前市场情况，{symbol} 呈现震荡上行趋势。建议关注成交量变化，若能持续放量可能突破关键压力位。",
        "目前大盘资金面偏紧，需要注意风险。建议控制仓位，等待企稳信号后再加仓。",
        "从技术面来看，{symbol} 处于上升通道中，短期支撑位在均线附近，建议逢低布局。"
    ],
    "role-2": [
        "趋势分析显示 {symbol} 处于上升趋势中，但短期可能面临回调压力。建议设置止损位。",
        "根据江恩理论分析，当前市场可能进入变盘节点，建议谨慎操作。",
        "短期趋势来看，{symbol} 有望继续上涨，但需注意MACD背离风险。"
    ],
    "role-3": [
        "技术形态分析：{symbol} 形成了W底形态，颈线位置在重要压力位，突破后上涨空间打开。",
        "RSI指标显示 {symbol} 目前处于超买区域，注意短期回调风险。",
        "布林带分析显示 {symbol} 股价触及上轨，短期可能有回踩中轨的需求。"
    ]
}

USER_RESPONSES = [
    "好的，我知道了。",
    "这个观点很有道理。",
    "谢谢你的分析！",
    "我再考虑考虑。",
    "有道理，支持一下！"
]

GROUP_RESPONSES = [
    "大家觉得今天大盘会怎么走？",
    "同意楼上观点。",
    "我觉得还要再观察一下。",
    "感谢分享！",
    "学习了。"
]

def generate_ai_response(role_id: str, user_message: str) -> dict:
    role_responses = AI_RESPONSES.get(role_id, AI_RESPONSES["role-1"])
    import random
    response_template = random.choice(role_responses)

    symbols = ["上证指数", "深证成指", "创业板", "科创板", "沪深300"]
    symbol = random.choice(symbols)

    response_content = response_template.format(symbol=symbol)

    return {
        "role": "assistant",
        "name": get_role_name(role_id),
        "content": response_content
    }

def get_role_name(role_id: str) -> str:
    roles = ai_roles_db.get("ai_roles", [])
    for role in roles:
        if role.get("id") == role_id:
            return role.get("name", "AI助手")
    return "AI助手"

def get_friend_name(friend_id: str, user_id: str) -> str:
    friends = friends_db.get(user_id, [])
    for friend in friends:
        if friend.get("id") == friend_id:
            return friend.get("name", "用户")
    return "用户"

def get_group_name(group_id: str, user_id: str) -> str:
    groups = groups_db.get(user_id, [])
    for group in groups:
        if group.get("id") == group_id:
            return group.get("name", "群聊")
    return "群聊"

def save_chat_message(session_id: str, message: dict):
    SessionDatabase.add_message(session_id, message)

def ensure_session(session_id: str, user_id: str):
    if not SessionDatabase.session_exists(session_id):
        SessionDatabase.create_session(session_id)
        
        user_sessions = sessions_db.get(user_id, [])
        if session_id not in user_sessions:
            user_sessions.append(session_id)
            sessions_db.set(user_id, user_sessions)

@router.get("/session/{chat_type}/{target_id}", summary="检查或创建会话")
async def check_or_create_session(chat_type: str, target_id: str, current_user: dict = Depends(get_current_user)):
    session_id = f"{current_user['id']}_{chat_type}_{target_id}"
    
    session_exists = SessionDatabase.session_exists(session_id)
    
    if not session_exists:
        SessionDatabase.create_session(session_id)
        
        user_sessions = sessions_db.get(current_user["id"], [])
        if session_id not in user_sessions:
            user_sessions.append(session_id)
            sessions_db.set(current_user["id"], user_sessions)
    
    return {
        "session_id": session_id,
        "created": not session_exists,
        "exists": session_exists
    }

@router.get("/sessions", summary="获取当前用户的所有会话列表")
async def get_user_sessions(current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    sessions = sessions_db.get(user_id, [])
    
    session_list = []
    for session_id in sessions:
        parts = session_id.split("_")
        if len(parts) >= 3:
            chat_type = parts[1]
            target_id = "_".join(parts[2:])
            
            session_data = SessionDatabase.load_session(session_id)
            messages = session_data.get("messages", [])
            last_message = messages[-1]["content"] if messages else ""
            
            session_info = {
                "session_id": session_id,
                "chat_type": chat_type,
                "target_id": target_id,
                "message_count": len(messages),
                "last_message": last_message[:50] + "..." if len(last_message) > 50 else last_message,
                "created_at": session_data.get("created_at", ""),
                "updated_at": session_data.get("updated_at", "")
            }
            
            session_list.append(session_info)
    
    return {"sessions": session_list}

@router.delete("/session/{session_id}", summary="删除会话")
async def delete_session(session_id: str, current_user: dict = Depends(get_current_user)):
    if not session_id.startswith(current_user["id"]):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    SessionDatabase.delete_session(session_id)
    
    user_sessions = sessions_db.get(current_user["id"], [])
    if session_id in user_sessions:
        user_sessions.remove(session_id)
        sessions_db.set(current_user["id"], user_sessions)
    
    return {"message": "Session deleted successfully"}

@router.post("/", summary="通用聊天接口")
async def chat(request: ChatRequest):
    user_id = request.user_config.get("user_ID", "unknown")
    target_role = request.user_message.get("target_role", "")
    query = request.user_message.get("query", "")

    session_id = f"{user_id}_ai_{target_role}"
    
    ensure_session(session_id, user_id)

    user_msg = {
        "id": f"msg-{uuid.uuid4().hex[:8]}",
        "role": "user",
        "name": user_id,
        "content": query,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    save_chat_message(session_id, user_msg)

    ai_response = generate_ai_response(target_role, query)

    ai_msg = {
        "id": f"msg-{uuid.uuid4().hex[:8]}",
        "role": ai_response["role"],
        "name": ai_response["name"],
        "content": ai_response["content"],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    save_chat_message(session_id, ai_msg)

    return ai_msg

@router.post("/group/{group_id}", summary="群聊")
async def chat_group(group_id: str, request: ChatRequest, current_user: dict = Depends(get_current_user)):
    user_id = request.user_config.get("user_ID", current_user["id"])
    query = request.user_message.get("query", "")

    session_id = f"{current_user['id']}_group_{group_id}"
    
    ensure_session(session_id, current_user["id"])

    user_msg = {
        "id": f"msg-{uuid.uuid4().hex[:8]}",
        "role": "user",
        "name": current_user["username"],
        "content": query,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    save_chat_message(session_id, user_msg)

    import random
    response_content = random.choice(GROUP_RESPONSES)

    ai_msg = {
        "id": f"msg-{uuid.uuid4().hex[:8]}",
        "role": "assistant",
        "name": get_group_name(group_id, current_user["id"]),
        "content": response_content,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    save_chat_message(session_id, ai_msg)

    return ai_msg

@router.post("/agent/{agent_id}", summary="与智能体聊天")
async def chat_agent(agent_id: str, request: ChatRequest, current_user: dict = Depends(get_current_user)):
    user_id = request.user_config.get("user_ID", current_user["id"])
    query = request.user_message.get("query", "")

    session_id = f"{current_user['id']}_agent_{agent_id}"
    
    ensure_session(session_id, current_user["id"])

    user_msg = {
        "id": f"msg-{uuid.uuid4().hex[:8]}",
        "role": "user",
        "name": current_user["username"],
        "content": query,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    save_chat_message(session_id, user_msg)

    ai_response = generate_ai_response(agent_id, query)

    ai_msg = {
        "id": f"msg-{uuid.uuid4().hex[:8]}",
        "role": ai_response["role"],
        "name": ai_response["name"],
        "content": ai_response["content"],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    save_chat_message(session_id, ai_msg)

    return ai_msg

@router.post("/friend/{friend_id}", summary="与用户聊天")
async def chat_friend(friend_id: str, request: ChatRequest, current_user: dict = Depends(get_current_user)):
    user_id = request.user_config.get("user_ID", current_user["id"])
    query = request.user_message.get("query", "")

    session_id = f"{current_user['id']}_friend_{friend_id}"
    
    ensure_session(session_id, current_user["id"])

    user_msg = {
        "id": f"msg-{uuid.uuid4().hex[:8]}",
        "role": "user",
        "name": current_user["username"],
        "content": query,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    save_chat_message(session_id, user_msg)

    import random
    response_content = random.choice(USER_RESPONSES)

    ai_msg = {
        "id": f"msg-{uuid.uuid4().hex[:8]}",
        "role": "assistant",
        "name": get_friend_name(friend_id, current_user["id"]),
        "content": response_content,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    save_chat_message(session_id, ai_msg)

    return ai_msg

@router.get("/history/{chat_type}/{target_id}", summary="获取聊天历史")
async def get_chat_history(chat_type: str, target_id: str, current_user: dict = Depends(get_current_user)):
    session_id = f"{current_user['id']}_{chat_type}_{target_id}"
    messages = SessionDatabase.get_messages(session_id)

    return {
        "session_id": session_id,
        "messages": messages
    }
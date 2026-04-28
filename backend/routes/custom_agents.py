from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from data.database import JSONDatabase
import uuid
from datetime import datetime
from routes.auth import get_current_user

router = APIRouter(prefix="/custom-agents", tags=["自定义智能体"])

db = JSONDatabase("custom_agents")
friends_db = JSONDatabase("friends")
sessions_db = JSONDatabase("sessions")

class CustomAgent(BaseModel):
    id: str
    name: str
    avatar: str
    ability: str
    personality: str
    description: str
    subscribed: bool
    created_at: str

class CustomAgentCreate(BaseModel):
    name: str
    avatar: str
    ability: str
    personality: str
    description: str

@router.get("/", summary="获取自定义智能体列表（包含订阅状态）")
async def get_custom_agents(current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    agents = db.get("custom_agents", [])
    user_friends = friends_db.get(user_id, [])
    
    agent_ids_in_friends = {f["role_id"] for f in user_friends if f.get("role_id") and f["role_id"].startswith("agent-")}
    
    result = []
    for agent in agents:
        is_subscribed = agent["id"] in agent_ids_in_friends
        result.append({
            **agent,
            "subscribed": is_subscribed
        })
    
    return {"custom_agents": result}

@router.get("/{agent_id}", response_model=CustomAgent, summary="获取单个自定义智能体")
async def get_custom_agent(agent_id: str, current_user: dict = Depends(get_current_user)):
    agent = db.find_by_id("custom_agents", agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Custom agent not found")
    
    user_id = current_user["id"]
    user_friends = friends_db.get(user_id, [])
    agent_ids_in_friends = {f["role_id"] for f in user_friends if f.get("role_id") and f["role_id"].startswith("agent-")}
    
    return {
        **agent,
        "subscribed": agent["id"] in agent_ids_in_friends
    }

@router.post("/", response_model=CustomAgent, summary="创建自定义智能体")
async def create_custom_agent(agent: CustomAgentCreate, current_user: dict = Depends(get_current_user)):
    agents = db.get("custom_agents", [])
    
    if any(a["name"] == agent.name for a in agents):
        raise HTTPException(status_code=400, detail="Agent name already exists")
    
    new_agent = {
        "id": f"agent-{uuid.uuid4().hex[:8]}",
        "name": agent.name,
        "avatar": agent.avatar,
        "ability": agent.ability,
        "personality": agent.personality,
        "description": agent.description,
        "subscribed": False,
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    
    db.append("custom_agents", new_agent)
    return new_agent

@router.put("/{agent_id}/subscribe", summary="订阅/取消订阅智能体")
async def toggle_subscribe(agent_id: str, current_user: dict = Depends(get_current_user)):
    index = db.find_index_by_id("custom_agents", agent_id)
    if index == -1:
        raise HTTPException(status_code=404, detail="Custom agent not found")
    
    agents = db.get("custom_agents", [])
    agent = agents[index]
    
    user_id = current_user["id"]
    user_friends = friends_db.get(user_id, [])
    
    agent_ids_in_friends = {f["role_id"] for f in user_friends if f.get("role_id") and f["role_id"].startswith("agent-")}
    is_currently_subscribed = agent_id in agent_ids_in_friends
    
    if is_currently_subscribed:
        friend_index = next((i for i, f in enumerate(user_friends) if f.get("role_id") == agent_id), -1)
        if friend_index != -1:
            friend_id = user_friends[friend_index]["id"]
            user_friends.pop(friend_index)
            friends_db.set(user_id, user_friends)
            
            session_id = f"{user_id}_agent_{friend_id}"
            user_sessions = sessions_db.get(user_id, [])
            if session_id in user_sessions:
                user_sessions.remove(session_id)
                sessions_db.set(user_id, user_sessions)
        
        new_subscribed = False
    else:
        new_friend = {
            "id": f"friend-{uuid.uuid4().hex[:8]}",
            "name": agent["name"],
            "avatar": agent["avatar"],
            "type": "ai",
            "role_id": agent_id,
            "status": "online",
            "created_at": datetime.utcnow().isoformat() + "Z"
        }
        
        user_friends.append(new_friend)
        friends_db.set(user_id, user_friends)
        
        session_id = f"{user_id}_agent_{new_friend['id']}"
        user_sessions = sessions_db.get(user_id, [])
        if session_id not in user_sessions:
            user_sessions.append(session_id)
            sessions_db.set(user_id, user_sessions)
        
        new_subscribed = True
    
    return {"message": "Subscription updated successfully", "subscribed": new_subscribed, "friend_id": new_friend["id"] if new_subscribed else None}

@router.put("/{agent_id}", response_model=CustomAgent, summary="更新自定义智能体")
async def update_custom_agent(agent_id: str, agent: CustomAgentCreate, current_user: dict = Depends(get_current_user)):
    index = db.find_index_by_id("custom_agents", agent_id)
    if index == -1:
        raise HTTPException(status_code=404, detail="Custom agent not found")
    
    agents = db.get("custom_agents", [])
    if any(a["name"] == agent.name and a["id"] != agent_id for a in agents):
        raise HTTPException(status_code=400, detail="Agent name already exists")
    
    existing_agent = agents[index]
    updated_agent = {
        "id": agent_id,
        "name": agent.name,
        "avatar": agent.avatar,
        "ability": agent.ability,
        "personality": agent.personality,
        "description": agent.description,
        "subscribed": existing_agent["subscribed"],
        "created_at": existing_agent["created_at"]
    }
    
    user_id = current_user["id"]
    user_friends = friends_db.get(user_id, [])
    for friend in user_friends:
        if friend.get("role_id") == agent_id:
            friend["name"] = agent.name
            friend["avatar"] = agent.avatar
            break
    friends_db.set(user_id, user_friends)
    
    db.update("custom_agents", index, updated_agent)
    return updated_agent

@router.delete("/{agent_id}", summary="删除自定义智能体")
async def delete_custom_agent(agent_id: str, current_user: dict = Depends(get_current_user)):
    agent = db.find_by_id("custom_agents", agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Custom agent not found")
    
    user_id = current_user["id"]
    user_friends = friends_db.get(user_id, [])
    user_friends = [f for f in user_friends if f.get("role_id") != agent_id]
    friends_db.set(user_id, user_friends)
    
    db.delete_by_id("custom_agents", agent_id)
    return {"message": "Custom agent deleted successfully"}
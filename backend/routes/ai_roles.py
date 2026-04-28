from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from data.database import JSONDatabase
import uuid
from datetime import datetime
from routes.auth import get_current_user

router = APIRouter(prefix="/ai-roles", tags=["AI角色"])

db = JSONDatabase("ai_roles")

class AIRole(BaseModel):
    id: str
    name: str
    description: str
    avatar: str
    ability: str
    personality: str
    created_at: str

class AIRoleCreate(BaseModel):
    name: str
    description: str
    avatar: str
    ability: str
    personality: str

@router.get("/", summary="获取所有AI角色")
async def get_ai_roles():
    roles = db.get("ai_roles", [])
    return {"ai_roles": roles}

@router.get("/{role_id}", response_model=AIRole, summary="获取单个AI角色")
async def get_ai_role(role_id: str):
    role = db.find_by_id("ai_roles", role_id)
    if not role:
        raise HTTPException(status_code=404, detail="AI role not found")
    return role

@router.post("/", response_model=AIRole, summary="创建AI角色")
async def create_ai_role(role: AIRoleCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    roles = db.get("ai_roles", [])
    if any(r["name"] == role.name for r in roles):
        raise HTTPException(status_code=400, detail="AI role name already exists")
    
    new_role = {
        "id": f"role-{uuid.uuid4().hex[:8]}",
        "name": role.name,
        "description": role.description,
        "avatar": role.avatar,
        "ability": role.ability,
        "personality": role.personality,
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    
    db.append("ai_roles", new_role)
    return new_role

@router.put("/{role_id}", response_model=AIRole, summary="更新AI角色")
async def update_ai_role(role_id: str, role: AIRoleCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    index = db.find_index_by_id("ai_roles", role_id)
    if index == -1:
        raise HTTPException(status_code=404, detail="AI role not found")
    
    roles = db.get("ai_roles", [])
    if any(r["name"] == role.name and r["id"] != role_id for r in roles):
        raise HTTPException(status_code=400, detail="AI role name already exists")
    
    updated_role = {
        "id": role_id,
        "name": role.name,
        "description": role.description,
        "avatar": role.avatar,
        "ability": role.ability,
        "personality": role.personality,
        "created_at": roles[index]["created_at"]
    }
    
    db.update("ai_roles", index, updated_role)
    return updated_role

@router.delete("/{role_id}", summary="删除AI角色")
async def delete_ai_role(role_id: str, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    role = db.find_by_id("ai_roles", role_id)
    if not role:
        raise HTTPException(status_code=404, detail="AI role not found")
    
    db.delete_by_id("ai_roles", role_id)
    return {"message": "AI role deleted successfully"}

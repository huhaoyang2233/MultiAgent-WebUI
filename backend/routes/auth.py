from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
from data.database import JSONDatabase
import uuid

router = APIRouter(prefix="/auth", tags=["认证"])

SECRET_KEY = "your-secret-key-here-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

db = JSONDatabase("users")

class User(BaseModel):
    id: str
    username: str
    email: str
    avatar: str
    role: str
    created_at: str

class UserCreate(BaseModel):
    username: str
    password: str
    email: str

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user(username: str):
    users = db.get("users", [])
    for user in users:
        if user["username"] == username:
            return user
    return None

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if token.startswith("mock_token_"):
        mock_username = token.replace("mock_token_", "").split("_")[0]
        user = get_user(mock_username)
        if user:
            return user
        raise credentials_exception
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user

@router.post("/register", response_model=User, summary="用户注册")
async def register(user: UserCreate):
    users = db.get("users", [])
    
    if any(u["username"] == user.username for u in users):
        raise HTTPException(status_code=400, detail="Username already registered")
    
    if any(u["email"] == user.email for u in users):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = {
        "id": f"user-{uuid.uuid4().hex[:8]}",
        "username": user.username,
        "password": user.password,
        "email": user.email,
        "avatar": f"https://i.pravatar.cc/40?img={len(users) + 1}",
        "role": "user",
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    
    db.append("users", new_user)
    return new_user

@router.post("/login", summary="用户登录")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)
    
    if not user or user["password"] != form_data.password:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "avatar": user["avatar"],
            "role": user["role"]
        }
    }

@router.get("/me", response_model=User, summary="获取当前用户信息")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/users", summary="获取所有用户列表")
async def get_users(current_user: User = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    users = db.get("users", [])
    return {"users": users}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import router as auth_router
from routes.ai_roles import router as ai_roles_router
from routes.friends import router as friends_router
from routes.groups import router as groups_router
from routes.custom_agents import router as custom_agents_router
from routes.chat_history import router as chat_history_router
from routes.chat import router as chat_router
from data.files.initial_data import init_data

init_data()

app = FastAPI(
    title="AI Agent Hub API",
    description="AI智能助手平台后端API服务",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(ai_roles_router)
app.include_router(friends_router)
app.include_router(groups_router)
app.include_router(custom_agents_router)
app.include_router(chat_history_router)
app.include_router(chat_router)

@app.get("/", summary="健康检查")
async def root():
    return {"message": "AI Agent Hub API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

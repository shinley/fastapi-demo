from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import news, users

app = FastAPI()

# 定义允许跨域请求的源列表（前端运行的地址）
origins = [
    "http://localhost:3000",       # 常见的 React/Next.js 前端地址
    "http://localhost:5173",       # 常见的 Vite/Vue/Svelte 前端地址
    "http://127.0.0.1:5173",
    "https://yourdomain.com",      # 生产环境的前端域名
]

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,                     # type: ignore
    allow_origins=origins,              # type: ignore 允许访问的源列表
    allow_credentials=True,             # type: ignore 是否允许携带 Cookie / 身份凭证
    allow_methods=["*"],                # type: ignore 允许的 HTTP 方法，如 ["GET", "POST", "PUT", "DELETE"]，"*" 表示全部
    allow_headers=["*"],                # type: ignore 允许的 HTTP 请求头，"*" 表示全部
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(news.router)
app.include_router(users.router)

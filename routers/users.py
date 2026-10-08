from fastapi import APIRouter

# 创建APIRouter 实例
router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/")
async def get_users():
    return {"msg": "获取用户列表"}
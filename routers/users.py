from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_config import get_db
from models.users import User
from schemas.users import UserRequest, UserAuthResponse, UserInfoResponse, UserUpdateRequest
from crud import users
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/user", tags=["users"])


# 用户注册
@router.post("register")
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    # 根据用户名查询数据库
    existing_user = await users.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this username already exists")

    user = await users.create_user(db, user_data)
    token = await users.create_token(db, user.id)

    # 新增用户
    user = await users.create_user(db, user_data)

    response_data = UserAuthResponse(
        token=token,
        user_info= UserInfoResponse.model_validate(user)
    )
    return success_response(message="success", data=response_data)

@router.post("/login")
async def login(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    user = await users.authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    token = await users.create_token(db, user.id)
    response_data = UserAuthResponse(token=token, user_info=UserInfoResponse.model_validate(user))
    return success_response(message="success", data=response_data)

@router.get("/info")
async def get_user_info(user: User=Depends(get_current_user)):
    return success_response(message="success", data=UserInfoResponse.model_validate(user))


@router.put("/update")
async def update_user_info(user_data: UserUpdateRequest,
                           user: User = Depends(get_current_user),
                           db: AsyncSession = Depends(get_db)):
    await users.update_user(db, user.username, user_data )
    return success_response(message="success", data=UserInfoResponse.model_validate(user))
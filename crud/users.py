from datetime import datetime, timedelta
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User, UserToken
from schemas.users import UserRequest
from utils import security


# 根据用户名查询数据库
async def get_user_by_username(db: AsyncSession, username: str):
    query = select(User).where(User.username == username)
    result = await db.execute(query)

    return result.scalar_one_or_none()


# 新增用户
async def create_user(db: AsyncSession, user_data: UserRequest):
    # 密码加密
    hashed_password = security.get_hash_password(user_data.password)
    user = User(username=user_data.username, password=hashed_password)

    db.add(user)
    await db.commit()
    await db.refresh(user)  # 刷新,从数据库读最新的
    return user

# 生成Token
async def create_token(db: AsyncSession, user_id: id):
    # 生成Token + 设置过期时间 -> 查询数据库当前用户是否有Token -> 有： 更新； 没有：添加
    token = str(uuid4())
    expires_at = datetime.now() + timedelta(days=30)
    query =select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()
    if user_token:
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        user_token = UserToken(user_id=user_id, token=token)
        db.add(user_token)
        await db.commit()

    return token

async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user:
        return None
    if not security.verify_password(password, user.password):
        return None
    return user


async def get_user_by_token(db: AsyncSession, token: str):
    query = select(UserToken).where(UserToken.token == token)
    result = await db.execute(query)
    db_token = result.scalar_one_or_none()

    if not db_token or db_token.expires_at < datetime.now():
        return None

    # 2. 再根据 user_id 查真正的 User
    user_query = select(User).where(User.id == db_token.user_id)
    user_result = await db.execute(user_query)
    return user_result.scalar_one_or_none()

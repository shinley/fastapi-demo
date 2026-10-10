import json

import redis.asyncio as redis

# 创建 Redis 的连接对象
redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)

# 读取缓存
async def get_cache(key: str):
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"获取缓存失败:{e}")
        return None

# 列表或字典
async def get_json_cache(key: str):
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data)
        else:
            return None
    except Exception as e:
        print(f"获取JSON缓存失败:{e}")
        return None

# 设置缓存
async def set_cache(key: str, value: any, expire: int = -1):
    try:
        if isinstance(value, (dict, list)):
            # 转字符串再存
            value= json.dumps(value, ensure_ascii=False)
        await redis_client.set(key, value, expire)
        return True
    except Exception as e:
        print(f"设置级存失败{e}")
        return False

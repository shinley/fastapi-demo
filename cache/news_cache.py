from typing import List, Dict, Any, Optional

from config.cache_conf import get_json_cache, set_cache

# 新闻相关的缓存方法： 新闻分类的读取和写入
# key - value
CAGEGORIES_KEY = "news:categories"
NEWS_LIST_PREFIX = "news_list"

# 获取新闻分类缓存
async def get_cached_categories():
    return await get_json_cache(CAGEGORIES_KEY)


# 写入新闻分类缓存
async def set_cached_categories(data: List[Dict[str, Any]], expire: int = 7200):
    return await set_cache(CAGEGORIES_KEY, data, expire)

# 写入缓存-新闻列表  key = news_list:分类id:页码:每页数量
async def set_cache_news_list(
        category_id: Optional[int],
        page: int,
        size: int,
        news_list: List[Dict[str, Any]],
        expire = None
):
    category_part = category_id if category_id is None else "all"
    # 设用封装的Redis 的设置方法，存新闻列表到缓存
    # 设用封装的Redis 的设置的方法
    key = f"{NEWS_LIST_PREFIX}_{category_part}:{page}:{size}"
    return await set_cache(key, news_list, expire)

# 读取缓存-新闻列表
async def get_cache_news_list(
        category_id: Optional[int],
        page: int,
        size: int,
):
    category_part = category_id if category_id is None else "all"
    key = f"{NEWS_LIST_PREFIX}_{category_part}:{page}:{size}"
    return await get_json_cache(key)

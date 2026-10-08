from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession



from config.db_config import get_db
from crud import news
# 创建APIRouter 实例
router = APIRouter(prefix="/api/news", tags=["news"])

@router.get("/categries")
async def get_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    categories = await news.get_categories(db, skip, limit)
    return {
        "code": 200,
        "message": "success",
        "data": categories
    }

@router.get("/list")
async def get_news_list(
        category_id: int = Query(..., alias="categoryId"),
        page: int = 1,
        page_size: int = Query(10, alias="pageSize"),
        db: AsyncSession = Depends(get_db)
):
    offset = (page - 1) * page_size
    news_list = await news.get_news_list(db, category_id, offset, page_size)
    total = await news.get_news_count(db, category_id)
    has_more=(offset+len(news_list)) < total
    return {
        "code": 200,
        "message": "success",
        "data": {
            "list": news_list,
            "total": total,
            "hasMore": has_more
        }
    }
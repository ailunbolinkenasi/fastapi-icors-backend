from fastapi import Depends, Request, APIRouter
from database.redis import sys_cache
from aioredis import Redis
from core.mall import Response
import random

redis = APIRouter(
    prefix="/v1",
    tags=["redis"]
)


@redis.get("/test/redis")
async def test_my_redis(req: Request):
    "连接池放在request当中"

    return {"mgs": "This is test redis"}


@redis.get("/test/dep_redis")
async def test_my_depens(phone: str, cache: Redis = Depends(sys_cache)):
    if await cache.get(name=phone):
        return Response(errmsg="请勿频繁发送验证码",code=400)

    await cache.set(name=phone, value=123456, ex=30)

    # 如果没有则写入
    return {"msg": f"手机号码为{phone}", "data": []}

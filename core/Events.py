# FastAPI事件监听
import aioredis
from typing import Callable

from aioredis import Redis
from fastapi import FastAPI
from database.redis import sys_cache
from database.mysql import register_mysql
from fastapi_limiter import FastAPILimiter


# Callable  作为函数返回值使用，其实只是做一个类型检查的作用，看看返回值是否为可调用对象
def startup(app: FastAPI) -> Callable:
    """
    FastApi 启动完成事件
    :param app: FastAPI
    :return: start_app
    """

    async def app_start() -> None:
        # APP启动完成后触发
        print("不知名项目启动成功.....放心没报错!")
        # 注册数据库
        await register_mysql(app)
        # 注入缓存到app state
        app.state.cache = await sys_cache()
        # 启动计数器
        redis = await aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
        await FastAPILimiter.init(redis)

    return app_start


def stopping(app: FastAPI) -> Callable:
    """
    FastApi 停止事件
    :param app: FastAPI
    :return: stop_app
    """

    async def stop_app() -> None:
        # APP停止时触发
        print("老铁你的FastAPI挂掉了!!!")
        cache: Redis = await app.state.cache
        await cache.close()

    return stop_app

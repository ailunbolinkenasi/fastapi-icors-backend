# FastAPI事件监听
from typing import Callable
from fastapi import FastAPI
from database.redis import sys_cache,token_code_cache
from aioredis import Redis
from  database.mysql import register_mysql


# Callable  作为函数返回值使用，其实只是做一个类型检查的作用，看看返回值是否为可调用对象
def startup(app: FastAPI) -> Callable:
    """
    FastApi 启动完成事件
    :param app: FastAPI
    :return: start_app
    """

    async def app_start() -> None:
        # APP启动完成后触发
        print("FastAPI-demo已经启动啦!!!☺")
        # 注册数据库
        await register_mysql(app)
        # 注入缓存到app state
        app.state.cache = await sys_cache()

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

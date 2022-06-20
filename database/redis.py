import aioredis
import os
from aioredis import Redis


async def sys_cache() -> Redis:
    """
    系统缓存
    :return: cache 连接池
    """
    # 从URL方式创建redis连接池
    sys_cache_pool = aioredis.ConnectionPool.from_url(
        f"redis://{os.getenv('CACHE_HOST', '10.1.6.110')}:{os.getenv('CACHE_PORT', 32547)}",
        db=os.getenv('CACHE_DB', 0),
        encoding='utf-8',
        decode_responses=True
    )
    return Redis(connection_pool=sys_cache_pool)


async def sms_code_cache() -> Redis:
    """
    短信验证码缓存
    :return: cache 连接池
    """
    sms_code_cache_pool = aioredis.ConnectionPool.from_url(
        f"redis://{os.getenv('CACHE_HOST', '10.1.6.110')}:{os.getenv('CACHE_PORT', 32547)}",
        db=os.getenv('CACHE_DB', 1),  # 验证码使用redis1库
        encoding='utf-8',
        decode_responses=True
    )
    return Redis(connection_pool=sms_code_cache_pool)


async def token_code_cache() -> Redis:
    """
    token缓存
    :return: cache 连接池
    """
    token_code_cache_pool = aioredis.ConnectionPool.from_url(
        f"redis://{os.getenv('CACHE_HOST', '10.1.6.110')}:{os.getenv('CACHE_PORT', 32547)}",
        db=os.getenv('CACHE_DB', 2),  # 验证码使用redis1库
        encoding='utf-8',
        decode_responses=True
    )
    return Redis(connection_pool=token_code_cache_pool)

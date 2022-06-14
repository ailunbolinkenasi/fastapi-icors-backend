import aioredis.exceptions
from fastapi import Depends, Query, Form, HTTPException, Request
from tortoise.expressions import Q, F
from applications.user.bodys import UserInfo, SmsBody, CreateUser
from aioredis import Redis
from applications.user.bodys import RegisterBody, UserBodyBase
from core.Utils import hash_password, verify_password
from core.mall import Response
from core.config import settings
from core.Jwt_auth import create_access_token, OAuth2
from database.redis import token_code_cache, sms_code_cache
from models.base import User, Role, Access


# 用户注册
async def register(user: RegisterBody, token_cache: Redis = Depends(token_code_cache)):
    # 检查账号是否存在
    get_user = await User.get_or_none(
        Q(username=user.username) | Q(mobile_phone=user.mobile_phone) | Q(email=user.email))
    if get_user:
        raise HTTPException(status_code=400, detail=f"用户已经注册.")
    if await User.get_or_none(Q(username=user.username) | Q(mobile_phone=user.mobile_phone) | Q(email=user.email)):
        raise HTTPException(status_code=400, detail="用户已经注册.")

    user.password = hash_password(user.password)
    # 注册后也会将token存储到Redis当中
    access_token = create_access_token(username=user.username)
    try:
        await token_cache.set(name=user.username, value=access_token, ex=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    except aioredis.exceptions.ConnectionError:
        raise HTTPException(status_code=500, detail="Redis连接失败,请检查服务端Redis状态,")
    await User.create(**user.dict())
    return Response(data={"access_token": access_token}, msg="注册成功")


# 用户登录
async def login(req: Request, user: UserBodyBase, token_cache: Redis = Depends(token_code_cache)):
    """
    :param user:  用户认证传入
    :param token_cache:  接入token缓存redis
    :return:
    """
    # 多个账号登录情况
    try:
        user_obj = await User.get_or_none(Q(username=user.username))
    except AttributeError as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    user_obj = await User.get_or_none(Q(username=user.username))
    # 判断用户是否存在
    if not user_obj:
        raise HTTPException(status_code=400, detail=f"{user.username}密码验证失败错误.")
    # 判断用户是否处于禁用状态
    if not user_obj.is_activate:
        raise HTTPException(status_code=400, detail=f"{user.username}已被禁用,请联系管理员.")
    # 如果redis中存在用户当前用户的token
    user_token = await token_cache.get(name=user.username)
    if user_token:
        raise HTTPException(status_code=400, detail=f"{user.username}已经登陆,禁止重复登陆.")
    # 如果获取到用户,然后进行验证密码
    if verify_password(user.password, user_obj.password):
        # 验证密码成功,生成access_token存入Redis
        access_token = create_access_token(username=user.username)
        await token_cache.set(name=user.username, value=access_token, ex=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        data = {"access_token": access_token, "expires_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60}
        return Response(data=data, msg="登录成功")
    raise HTTPException(status_code=400, detail="用户名或密码错误!")


# 短信登录
async def login_sms(auth: SmsBody, code_redis: Redis = Depends(sms_code_cache),
                    token_redis: Redis = Depends(token_code_cache)):
    """
    :param auth: 短信认证模型
    :param code_redis:  验证码缓存
    :param token_redis:  登录token缓存
    :return:
    """
    # 判断用户是否存在
    get_user = await User.get_or_none(Q(username=auth.mobile_phone) | Q(mobile_phone=auth.mobile_phone))
    if not get_user:
        raise HTTPException(status_code=400, detail="密码验证失败!")
    if not get_user.is_activate:
        raise HTTPException(status_code=400, detail=f"{auth.mobile_phone}已被禁用,请联系管理员.")
    # 尝试获取token在redis中的缓存
    token_cache = await token_redis.get(auth.mobile_phone)
    # 判断用户是否登录
    if token_cache:
        return Response(data={"access_token": token_cache}, msg="已经登录,禁止重复登录", code=400)
    # 获取redis中的短信验证码
    redis_sms_code = await code_redis.get(auth.mobile_phone)
    # 判断验证码
    if auth.sms_code == redis_sms_code:
        # token写入redis
        access_token = create_access_token(username=auth.mobile_phone)
        await token_redis.set(name=auth.mobile_phone, value=access_token,
                              ex=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        # 验证码写入redis
        return Response(data={"access_token": access_token}, msg="登录成功", code=200)
    raise HTTPException(status_code=400, detail="验证码错误或者已经失效!")


# 查询用户信息
async def get_user_info(username: str = Query(default=None, max_length=20)):
    """
    :param username:   通过用户名查询
    :return:
    """
    get_user = await User.get_or_none(Q(username=username) | Q(mobile_phone=username)).values('id', 'username',
                                                                                              'mobile_phone', 'email',
                                                                                              'is_activate')
    if get_user:
        return Response(data=get_user, msg="查询成功.", code=200)
    get_user = await User.get_or_none(Q(username=username) | Q(mobile_phone=username))
    if get_user:
        data = UserInfo(
            id=get_user.pk,
            username=get_user.username,
            mobile_phone=get_user.mobile_phone,
            email=get_user.email,
            is_activate=get_user.is_activate
        )
        return Response(data=data, msg="查询成功.", code=200)
    raise HTTPException(status_code=400, detail="查询结果为空.")


# 添加用户
async def create_user(user: CreateUser):
    get_username = await User.get_or_none(username=user.username)
    # 如果添加用户存在的话
    if get_username:
        raise HTTPException(status_code=400, detail=f"{get_username.username}已经存在,请勿重复添加!")
    user.password = hash_password(user.password)
    return Response(data=user.__dict__, msg="添加成功")


# 删除用户
async def delete_user(user_id: int, token: str = Depends(OAuth2)):
    """
    :user_id: 传入需要删除的用户Id
    """
    if user_id == 1:
        raise HTTPException(status_code=400, detail="啊啊啊啊啊不要删除管理员啊😊")
    data = {"token": token}
    return Response(data=data, msg="成功")


# 获取用户列表
async def get_user_list(pageSize: int = 10, current: int = 1, username: str = Query(None),
                        mobile_phone: str = Query(None), email: str = Query(None), is_activate: bool = Query(None)):
    """
    获取所有用户
    : return:
    """
    query = {}
    if username:
        query.setdefault('username', username)
    if mobile_phone:
        query.setdefault('mobile_phone', mobile_phone)
    if email:
        query.setdefault('email', email)
    if is_activate is not None:
        query.setdefault('is_activate', is_activate)

    user_data = User.annotate(key=F("id")).filter(**query).filter(id__not=1).all()
    # 总数
    total = await user_data.count()
    # 查询
    data = await user_data.limit(pageSize).offset(pageSize * (current - 1)).order_by("-create_time").values(
        "id", "username", "mobile_phone", "email", "is_activate"
    )
    return Response(data=data, msg="查询成功")


# 获取Oath2
async def read_items(token: str = Depends(OAuth2)):
    return {"token": token}

from datetime import timedelta

import aioredis.exceptions
from fastapi import Depends, Query, Form, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from tortoise.exceptions import IntegrityError
from tortoise.expressions import Q, F
from applications.user.bodys import UserInfo, SmsBody, CreateUser, UpdateUser
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
    get_user = await User.filter(
        Q(username=user.username) | Q(mobile_phone=user.mobile_phone) | Q(email=user.email))
    if get_user:
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
        user_obj = await User.get_or_none(
            Q(username=user.username) | Q(mobile_phone=user.username))
    except AttributeError as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    # 判断用户是否存在
    if not user_obj:
        raise HTTPException(status_code=400, detail=f"{user.username}密码验证失败错误.")
    # 判断用户是否处于禁用状态
    if not user_obj.is_activate:
        raise HTTPException(status_code=400, detail=f"{user.username}已被禁用,请联系管理员.")
    # 如果redis中存在用户当前用户的token
    try:
        user_token = await token_cache.get(name=user.username)
    # 如果抛出Redis连接异常
    except aioredis.connection.ConnectionError as e:
        raise HTTPException(status_code=500, detail="获取登录token失败,请检查Redis连接是否正常！")
    # 如果获取到用户,然后进行验证密码
    if verify_password(user.password, user_obj.password):
        if user_token:
            raise HTTPException(status_code=400, detail=f"{user.username}已经登陆,禁止重复登陆.")
        # 验证密码成功,生成access_token存入Redis
        access_token = create_access_token(username=user.username)
        try:
            await token_cache.set(name=user.username, value=access_token, ex=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        except aioredis.connection.ConnectionError:
            raise HTTPException(status_code=500, detail="Redis服务连接失败,请检查后端日志!")
        data = {"access_token": access_token, "expires_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES}
        return Response(data=data, msg="登录成功")
    raise HTTPException(status_code=400, detail="用户名或密码错误!")


# 短信登录
async def login_sms(auth: SmsBody, code_cache: Redis = Depends(sms_code_cache),
                    token_cache: Redis = Depends(token_code_cache)):
    """
    :param auth: 短信认证模型
    :param code_cache:  验证码缓存
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
    token = await token_cache.get(auth.mobile_phone)
    # 获取redis中的短信验证码
    redis_sms_code = await code_cache.get(auth.mobile_phone)
    # 判断验证码
    if auth.sms_code == redis_sms_code:
        # 判断用户是否登录
        if token:
            return Response(data={"access_token": token}, msg="已经登录,禁止重复登录", code=400)
        # token写入redis
        access_token = create_access_token(username=auth.mobile_phone)
        await token_cache.set(name=auth.mobile_phone, value=access_token,
                              ex=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        # 登陆成功后删除用户验证码
        await code_cache.delete(auth.mobile_phone)
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
    """
    :param user:  创建用户入参模型
    :return:
    """
    get_username = await User.get_or_none(username=user.username)
    # 如果添加用户存在的话
    if get_username:
        raise HTTPException(status_code=400, detail=f"{get_username.username}已经存在,请勿重复添加!")
    user.password = hash_password(user.password)
    await User.create(**user.dict())
    return Response(msg=f"{user.username}添加成功!")


# 更新用户
async def update_user(user: UpdateUser):
    """
    :param user: 更新用户模型
    :return:
    """
    user_check = await User.get_or_none(username=user.username)
    if not user_check:
        raise HTTPException(status_code=400, detail="更新用户不存在.")
    if user.password:
        user.password = hash_password(user.password)
    data = user.dict()
    try:
        await User.filter(username=user.username).update(**data)
    # 如果更新的字段触发数据库唯一索引
    except IntegrityError as e:
        return HTTPException(status_code=400, detail=f"{e}")
    return Response(msg="数据更新成功")


# 删除用户
async def delete_user(user_id: int):
    """
    :user_id: 传入需要删除的用户Id
    """
    if user_id == 1:
        raise HTTPException(status_code=400, detail="你是何方人物...系统账户不允许删除哦~")
    get_user = await User.filter(pk=user_id).delete()
    if not get_user:
        raise HTTPException(status_code=400, detail=f"当前id为{user_id}的用户删除失败咯.")
    return Response(msg="删除成功")


# 获取用户列表
# async def get_user_list(pageSize: int = 10, current: int = 1, username: str = Query(None),
#                         mobile_phone: str = Query(None), email: str = Query(None),
#                         is_activate: bool = Query(None)) -> None:
#     """
#     获取所有用户
#     : return:
#     """
#     return Response(data=data, msg="查询成功")


# 获取Oath2
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
     OAuth2 compatible token login, get an access token for future requests
    """
    user = await User.get_or_none(username=form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="密码不对,别乱填.")
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        user.username,
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}

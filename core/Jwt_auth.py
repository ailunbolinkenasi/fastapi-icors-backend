import jwt
import base64
from fastapi import Depends, Request, HTTPException
from typing import Union
from fastapi.security import SecurityScopes, OAuth2PasswordBearer
from datetime import datetime, timedelta
from models.base import User, Access,Role
from pydantic import ValidationError
from starlette import status
from core.config import settings

OAuth2 = OAuth2PasswordBearer(tokenUrl=settings.SWAGGER_UI_OAUTH2_REDIRECT_URL)


# 创建用户访问token
def create_access_token(username: str, expires_delta: Union[timedelta, None] = None):
    """
    :param user_id:    传入用户名
    :param expires_delta:  过期时间
    :return:
    """
    token_encode = {"username": username}.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    # 更新过期时间
    token_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(token_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


# 检查用户token
async def check_token_http(req: Request, security_scopes: SecurityScopes, token=Depends(OAuth2)):
    """
    :param req:
    :param security_scopes:
    :param token:
    :return:
    """
    try:
        # 用户token解码
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        # 获取用户id,当获取不到则默认为空
        username = payload.get("username", None)
        print("Payload解析用户名为:", username)
        # 如果无法获取到用户信息
        if username is None:
            credentials_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="该凭证是无效的",
                headers={"WWW-Authenticate": f"Bearer {token}"}
            )
            raise credentials_exception
        else:
            pass
    # 当用户token过期
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="凭证已过期",
            headers={"WWW-Authenticate": f"Bearer {token}"}
        )
    # 当token无效
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效凭证",
            headers={"WWW-Authenticate": f"Bearer {token}"}
        )
    # 当JWT验证错误的时候
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效凭证",
            headers={"WWW-Authenticate": f"Bearer {token}"}
        )
    # 验证权限
    get_user = await User.get_or_none(username=username)
    if not get_user or get_user.is_activate != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名不存在或已被禁用!",
            headers={"WWW-Authenticate": f"Bearer {token}"}
        )
    # 判断是否设置了权限域
    if security_scopes.scopes:
        # 返回当前权限域
        print("当前域: ", security_scopes.scopes)
        scopes = []
        # 非admin账户并且请求的接口需要权限验证
        if not get_user.is_staff and security_scopes.scopes:
            is_pass = await Access.filter(role__user__username=username, is_check=True,
                                          scopes__in=set(security_scopes.scopes)).all()
            username = await Role.filter(user__username=username)
            print("当前查询用户名",username)
            print("权限查询结果为:", is_pass)
            if not is_pass:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="你要摆清楚你的定位,你不是一个拥有查看此内容的人!",
                    headers={"scopes": security_scopes.scope_str},
                )

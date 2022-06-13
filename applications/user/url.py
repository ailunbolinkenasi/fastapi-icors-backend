from fastapi import APIRouter, Security, Depends
from applications.user.view import register, login, get_user_info, get_user_role, login_sms
from core.Jwt_auth import check_token_http
from fastapi_limiter.depends import RateLimiter

user = APIRouter(
    prefix="/v1",
)

role = APIRouter(
    prefix="/v1",
)
user.post("/register",
          summary="用户注册",
          tags=['用户注册']
          )(register)

user.post("/login",
          summary="用户登录",
          tags=['用户登录'],
          dependencies=[Depends(RateLimiter(times=2,milliseconds=5))]
          )(login)

user.post("/sms_login",
          summary="短信登录服务",
          tags=['用户登录'],
          )(login_sms)

user.get("/user/info",
         summary="用户信息",
         tags=['用户服务'],
         dependencies=[Security(check_token_http, scopes=["user_info_ac"])]
         )(get_user_info)

role.get("/user/role_info",
         summary="获取用户权限信息",
         tags=['用户服务'],
         # dependencies=[Security(check_token_http, scopes=["user_info_ac", "user_role_ac"])]
         )(get_user_role)

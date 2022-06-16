from fastapi import APIRouter, Security, Depends
from applications.user.view import register, login, get_user_info, login_sms, get_user_list, delete_user, \
    login_for_access_token
from core.Jwt_auth import check_token_http
from fastapi_limiter.depends import RateLimiter
from schemas.token import Token

user = APIRouter(
    prefix="/v1",
)

user.post("/register",
          summary="用户注册",
          tags=['用户注册']
          )(register)

user.post("/login",
          summary="用户登录",
          tags=['用户登录'],
          dependencies=[Depends(RateLimiter(times=2, milliseconds=5))]
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

user.get("/user/list",
         summary="查询所有用户",
         tags=['用户服务'],
         )(get_user_list)

user.delete("/delete/user",
            summary="删除用户",
            tags=['用户服务']
            )(delete_user)

user.post('/login/access_token',
          summary="获取token接口",
          tags=['获取用户token接口'],
          response_model=Token)(login_for_access_token)

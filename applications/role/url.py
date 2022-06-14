from fastapi import APIRouter, Security, Depends
from core.Jwt_auth import check_token_http
from fastapi_limiter.depends import RateLimiter
from applications.role.view import get_user_role, set_role

role = APIRouter(
    prefix="/v1",
)

role.get("/role/role_info",
         summary="获取用户权限信息",
         tags=['权限服务'],
         # dependencies=[Security(check_token_http, scopes=["user_info_ac", "user_role_ac"])]
         )(get_user_role)

role.put("/role/set_role",
         summary="分配权限",
         tags=['权限服务']
         )(set_role)

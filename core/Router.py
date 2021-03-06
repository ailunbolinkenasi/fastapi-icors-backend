from fastapi import APIRouter
from applications.user.url import user,role
from applications.public.url import public_services
router = APIRouter()
# 用户认证路由
router.include_router(user)
# 权限相关路由
router.include_router(role)

# 公共服务路由
router.include_router(public_services)
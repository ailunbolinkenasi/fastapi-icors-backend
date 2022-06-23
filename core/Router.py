from fastapi import APIRouter
from applications.public.url import public_services
from applications.role.url import role
from applications.system.url import system
from applications.user.url import user
from applications.monitor.url import monitor_services

router = APIRouter()
# 公共服务路由
router.include_router(public_services)

# 监控服务路由
router.include_router(monitor_services)

# 用户认证路由
router.include_router(user)

# 权限相关路由
router.include_router(role)

# 添加服务器信息路由
router.include_router(system)

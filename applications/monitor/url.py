from fastapi import APIRouter, Security
from core.Jwt_auth import check_token_http
from applications.monitor.view import get_monitor_data
from applications.monitor.bodys import MonitorList

monitor_services = APIRouter(
    prefix="/v1",
    tags=["监控服务"]
)

monitor_services.get('/monitor/all',
                     summary="获取设备监控数据",
                     # response_model=MonitorList
                     )(get_monitor_data)

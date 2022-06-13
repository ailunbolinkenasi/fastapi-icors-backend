from fastapi import APIRouter, Security
from applications.system.view import add_host
from applications.system.bodys import AddHost
system = APIRouter(
    prefix="/v1",
)

system.post("/create/host",
            summary="服务器信息添加",
            tags=['服务器信息']
            )(add_host)

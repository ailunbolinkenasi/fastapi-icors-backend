from fastapi import APIRouter, Security
from applications.system.view import add_hosts, update_hosts, get_hosts, del_hosts
from applications.system.bodys import AddHost
from core.Jwt_auth import check_token_http

system = APIRouter(
    prefix="/v1",
)

system.get("/list/host",
           summary="服务器信息获取",
           tags=['服务器信息'],
           dependencies=[Security(check_token_http, scopes=['host_list.ac'])]
           )(get_hosts)

system.post("/create/host",
            summary="服务器信息添加",
            tags=['服务器信息'],
            dependencies=[Security(check_token_http, scopes=["host_add_ac"])]
            )(add_hosts)

system.put("/update/host",
           summary="服务器信息修改",
           tags=['服务器信息'],
           dependencies=[Security(check_token_http, scopes=['host_update.ac'])]
           )(update_hosts)

system.delete("/delete/host",
              summary="服务器信息删除",
              tags=['服务器信息'],
              dependencies=[Security(check_token_http, scopes=['host_delete.ac'])]
              )(del_hosts)

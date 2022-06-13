from fastapi import Depends, Query, HTTPException
from tortoise.expressions import Q
from applications.system.bodys import AddHost
from core.mall import Response, ErrorResponse
from models.device import Device
from fastapi import Request
from typing import Optional


# 添加服务器信息
async def add_hosts(host: AddHost):
    get_hosts = await Device.get_or_none(ipaddr=host.ipaddr)
    if get_hosts:
        raise HTTPException(status_code=400, detail=f"{get_hosts.ipaddr}已添加!")
    await Device.create(**host.dict())
    return Response(data=host.__dict__, msg="添加成功")


# 删除服务器信息
async def del_hosts(id: int):
    delete_host = await Device.filter(pk=id).delete()
    if delete_host is False:
        raise HTTPException(status_code=400, detail=f"{id}删除失败!")
    return Response(msg="删除成功")


# 修改服务器信息
# async def update_hosts(id: int, host: UpdateHost):
#     get_host = await Device.get_or_none(pk=id)
#     if not get_host:
#         raise HTTPException(status_code=400, detail=f"未能找ID值为{id}的主机!")
#     # 如果更新的主机已经存在
#     # if host.ipaddr == get_host.ipaddr:
#     #     raise HTTPException(status_code=400, detail=f"{host.ipaddr}已经存在.")
#     data = host.dict()
#     await Device.filter(pk=id).update(**data)
#     # 查询更新后的信息
#     update_data = await Device.filter(pk=id)
#     return Response(data=update_data, msg="更新成功")


# 获取服务器信息
async def get_hosts(req: Request):
    get_host = await Device.all()
    return Response(data=get_host, msg="查询成功")


# 添加服务器信息
async def add_host(host: AddHost):
    get_hosts = await Device.get_or_none(ipaddr=host.ipaddr)
    if get_hosts:
        return ErrorResponse(errmsg=f"{host.ipaddr}已经存在", code=400)
    await Device.create(**host.dict())
    return Response(data=host.__dict__, msg="添加成功")

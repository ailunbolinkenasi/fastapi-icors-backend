from fastapi import Depends, Query, HTTPException
from tortoise.expressions import Q
from applications.system.bodys import AddHost, UpdateHost
from core.mall import Response
from models.device import Device
from fastapi import Request


# 添加服务器信息
async def add_hosts(host: AddHost):
    hosts_list = await Device.get_or_none(ipaddr=host.ipaddr)
    if hosts_list:
        raise HTTPException(status_code=400, detail=f"{hosts_list.ipaddr}已添加!")
    add = await Device.create(**host.dict())
    if not add:
        raise HTTPException(status_code=400, detail=f"{hosts_list.ipaddr}添加失败!")
    return Response(data=host.__dict__, msg="添加成功")


# 删除服务器信息
async def del_hosts(id: int):
    delete_host = await Device.filter(pk=id).delete()
    if not delete_host:
        raise HTTPException(status_code=400, detail=f"当前删除id为{id}的主机不存在")
    return Response(msg="删除成功")


# 修改服务器信息
async def update_hosts(qid: int, host: UpdateHost):
    get_host = await Device.get_or_none(pk=qid)
    if get_host is None:
        raise HTTPException(status_code=400, detail=f"未能找ID值为{qid}的主机!")
    # 如果更新的主机已经存在
    # if host.ipaddr == get_host.ipaddr:
    #     raise HTTPException(status_code=400, detail=f"{host.ipaddr}已经存在.")
    data = host.dict()
    await Device.filter(pk=qid).update(**data)
    # 查询更新后的信息
    update_data = await Device.filter(pk=qid)
    return Response(data=update_data, msg="更新成功")


# 获取服务器信息
async def host_list(req: Request):
    get_host = await Device.all()
    if not get_host:
        raise HTTPException(status_code=400, detail="当前数据库中无任何主机信息!")
    return Response(data=get_host, msg="获取主机列表成功")

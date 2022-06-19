from models.base import User, Role, Access
from fastapi import HTTPException
from applications.role.bodys import SetRole
from core.mall import Response


# 获取用用户权限集合
async def get_user_role(user_id: int):
    """
    :param user_id:  传入用户Id
    :return:
    """
    user_role = await Role.filter(user__id=user_id).values("role_name", "role_status")
    # 查询用户的所有权限,反向查询role角色表中的跟user表关联的user_id
    user_access_list = await Access.filter(role__user__id=user_id, is_check=True).values("id", "scopes")
    # 验证当前用户对当前操作的作用域是否有权限
    is_permi = await Access.get_or_none(role__user__id=user_id, is_check=True, scopes="user_info",
                                        role__role_status=True)
    data = {
        "role_info": user_role,
        "user_access_list": user_access_list
    }

    if user_role:
        return Response(data=data, msg="获取成功", code=200)
    raise HTTPException(status_code=400, detail="获取失败,该用户无权限分配或权限分配失败.")


# 角色分配
async def set_role(role_set: SetRole):
    user_obj = await User.get_or_none(pk=role_set.id)
    if user_obj is None:
        raise HTTPException(status_code=400, detail="用户不存在!")
    # 清空角色
    await user_obj.role.clear()
    # 如果提交了roles列表
    if role_set.roles:
        roles = await Role.filter(role_status=True, id__in=role_set.roles).all()
        # 分配角色
        await user_obj.role.add(*roles)
    return Response(data=user_obj, msg="角色分配成功")

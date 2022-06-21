import random
import jwt
import Tea.exceptions
from pusher import Pusher,errors
from fastapi import Depends, HTTPException
from jwt import PyJWTError
from pydantic import ValidationError
from starlette.endpoints import WebSocketEndpoint
from starlette.websockets import WebSocket, WebSocketDisconnect
from core.config import settings
from core.Utils import create_client
from core.mall import Response, ErrorResponse
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_util import models as util_models
from database.redis import sms_code_cache
from aioredis import Redis


# 阿里云短信发送接口
async def aliyun_send(mobile_phone: str, sms_cache: Redis = Depends(sms_code_cache)) -> Response:
    """
    :param mobile_phone:  发送短信的手机号
    :return:
    """
    # 判断传入手机号和短信模板是否为空
    if mobile_phone == '':
        raise HTTPException(status_code=400, detail="禁止传入空手机号！")
    client = create_client(settings.ALIYUN_ACCESSKEY_ID, settings.ALIYUN_ACCESSKEY_SECRET)
    # 生成六位数随机验证码
    verification_code = str(random.randrange(1000, 999999))
    print("当前验证码为:", verification_code)
    try:
        # 发送请求
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            phone_numbers=mobile_phone,
            sign_name=settings.ALIYUN_SIGN_NAME,
            template_code="SMS_242870552",
            template_param=("{\"code\":\"%s\"}" % verification_code)
            # 以下格式化方式不可用
            # template_param=f'{"code":{verification_code}}'
        )
        runtime = util_models.RuntimeOptions()
        # 异步数据需要使用await 进行获取
        data = await client.send_sms_with_options_async(send_sms_request, runtime)
    except Tea.exceptions.TeaException:
        raise HTTPException(status_code=400, detail=" AccessKeyId is mandatory for this action")

    if data.body.code == "OK":
        # 将验证码写入Redis,过期时间为60秒
        await sms_cache.set(name=mobile_phone, value=verification_code, ex=60)
        return Response(data=data.__dict__.get("body"), msg="短信发送成功")
    return ErrorResponse(data=data.__dict__.get("body"), errmsg="发送失败", code=400)


# websocket检验token接口
async def check_token(token: str):
    """
    :param token:
    :return:
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        print(payload)
        if payload:
            # 用户名
            username = payload.get("username", None)
            if username is None:
                return HTTPException(status_code=400, detail="用户校验失败")
        else:
            raise HTTPException(status_code=400, detail="检查Token失败!")

    # Token过期异常处理
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token已过期.")
    # Token无效异常处理
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="无效Token!")
    # PyJWT以及校验错误处理
    except(PyJWTError, ValidationError):
        raise HTTPException(status_code=400, detail="Token数据内容校验失败")


# class Chat(WebSocketEndpoint):
#     encoding = "json"
#     # 活跃连接数量
#     activate_connections = [
#
#     ]
#
#     # 创建websocket
#     async def create_websocket(self, web_socket: WebSocket):
#         """
#         :param web_socket:
#         :return:
#         """
#         user_type = web_socket.query_params.get("user_type")
#         token = web_socket.query_params.get("sec-websocket")
#         real_ip = web_socket.query_params.get("x-forwarded-for")
#         real_host = web_socket.query_params.get("host")
#         try:
#             # 如果获取不到用户类型或者token则返回WebSocketDisconnect错误
#             if not user_type or token:
#                 raise WebSocketDisconnect
#             username = check_token(token)
#             if not username:
#                 raise WebSocketDisconnect
#             # 接受http连接
#             await web_socket.accept(subprotocol=token)
#
#             for connection in self.activate_connections:
#                 if connection['username'] == username and connection['user_type'] == user_type:
#                     # 删除历史连接
#                     self.activate_connections.remove(connection)
#             print(f"客户端IP: {real_ip},来源主机: {real_host},用户类型: {user_type},用户名: {username}")
#         except WebSocketDisconnect:
#             # 关闭socket连接
#             await web_socket.close()
#             print("连接关闭!")


# 消息推送服务
async def push_chat(message: str):
    pusher_client = Pusher(
        app_id='1426377',
        key='00008e3994f1fc4c7baf',
        secret='dd57cbc96d42b6525f87',
        cluster='ap1',
        ssl=True
    )
    # 尝试发送消息e
    try:
        pusher_client.trigger('my-channel', 'my-event', {'消息': format(message)})
    except errors.PusherError as e:
        # print(e)
        raise HTTPException(status_code=400,detail="消息推送失败！")
    return Response(msg="消息推送成功")

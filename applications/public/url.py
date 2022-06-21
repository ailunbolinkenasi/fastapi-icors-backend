from fastapi import APIRouter, Security
from applications.public.view import aliyun_send, push_chat
from core.Jwt_auth import check_token_http

public_services = APIRouter(
    prefix="/v1",
    tags=["公共服务"]
)

public_services.post("/sms",
                     summary="短信发送接口",
                     # dependencies=Security(check_token_http, scopes=["public_services"])
                     )(aliyun_send)

public_services.get("/push",
                    summary="事件推送",
                    )(push_chat)

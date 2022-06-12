from fastapi import APIRouter, Security
from applications.public.view import aliyun_send
from core.Jwt_auth import check_token_http

public_services = APIRouter(
    prefix="/v1",
    tags=["公共服务"]
)

public_services.post("/sms",
                     summary="短信发送接口",
                     # dependencies=Security(check_token_http, scopes=["public_services"])
                     )(aliyun_send)

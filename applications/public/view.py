import random
import Tea.exceptions
from fastapi import Depends,HTTPException
from core.config import settings
from core.Utils import create_client
from core.mall import Response, ErrorResponse
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_util import models as util_models
from database.redis import sms_code_cache
from aioredis import Redis


# 阿里云短信发送接口
async def aliyun_send(mobile_phone: str, sms_cache: Redis = Depends(sms_code_cache)) -> None:
    """
    :param mobile_phone:  发送短信的手机号
    :param template_code:  短信模板,默认模板 SMS_242870552
    :return:
    """
    # 判断传入手机号和短信模板是否为空
    if mobile_phone == '':
        return ErrorResponse(errmsg="禁止空手机号或短信模板!", code=400)
    client = create_client(settings.ALIYUN_ACCESSKEY_ID, settings.ALIYUN_ACCESSKEY_SECRET)
    # 生成六位数随机验证码
    verification_code = str(random.randrange(1000, 999999))
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
        raise HTTPException(status_code=400,detail=" AccessKeyId is mandatory for this action")

    if data.body.code == "OK":
        # 将验证码写入Redis
        await sms_cache.set(name=mobile_phone, value=verification_code, ex=60)
        return Response(data=data.__dict__.get("body"), msg="短信发送成功")
    return ErrorResponse(data=data.__dict__.get("body"), errmsg="发送失败", code=400)

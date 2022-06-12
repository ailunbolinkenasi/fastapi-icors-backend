import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core.Events import startup, stopping
from core.config import settings
from fastapi.openapi.docs import get_swagger_ui_oauth2_redirect_html
from core.Router import router

# 实例化
application = FastAPI(
    debug=settings.APP_DEBUG,
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    swagger_ui_oauth2_redirect_url=settings.SWAGGER_UI_OAUTH2_REDIRECT_URL,
)

# 重写swagger_ui_js地址

# 跨域请求处理
application.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)


# swagger_ui_oauth2_redirect_url
@application.get(application.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


# 注册监听事件
application.add_event_handler("startup", startup(application))
application.add_event_handler("shutdown", stopping(application))
# 异常错误处理
# application.add_exception_handler(HTTPException, http_error_handler)
# application.add_exception_handler(RequestValidationError, http422_error_handler)
# application.add_exception_handler(UnicornException, unicorn_exception_handler)
# application.add_exception_handler(DoesNotExist, mysql_does_not_exist)
# application.add_exception_handler(OperationalError, mysql_operational_error)


# 路由
application.include_router(router)
if __name__ == "__main__":
    uvicorn.run(app='main:application', host='0.0.0.0',
                port=8000, reload=True, debug=True)

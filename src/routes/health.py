from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from helpers import get_settings, Settings

from enums import ResponseEnums


health_router = APIRouter(
    prefix = "/api/v1",
    tags = ["api_v1"]
)

@health_router.get("/")
async def welcome(app_settings: Settings = Depends(get_settings)):

    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION


    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {
            "message": ResponseEnums.HEALTH_CHECK_OK.value,
            "app_name": app_name,
            "app_version": app_version

        }
    )
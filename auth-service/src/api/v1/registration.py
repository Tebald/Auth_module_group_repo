from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.postgres import get_pg_session
from src.services.registration import RegistrationService, get_registration_service
from src.schema.model import (
    UserRegistrationReq,
    UserRegisteredResp,
    ValidationErrorResp,
    BadRequestResp
)
from typing import List


router = APIRouter()


@router.post(
    "/register",
    status_code=201,
    response_model=UserRegisteredResp | ValidationErrorResp | BadRequestResp, 
    responses={
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ValidationErrorResp},
        status.HTTP_400_BAD_REQUEST: {"model": BadRequestResp},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"}
    }
)
async def register_user(
    user_data: UserRegistrationReq,
    db: AsyncSession = Depends(get_pg_session),
    registration_service: RegistrationService = Depends(get_registration_service)
):
    """
    Регистрация пользователя
    """
    result = await registration_service.register_user(db=db, user_info=user_data)
    return result

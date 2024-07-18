from fastapi import APIRouter

from ...api.api_v1.endpoints import user, user_role, role, process

api_router = APIRouter()
api_router.include_router(user.router, prefix='/user', tags=['user'])
api_router.include_router(user_role.router, prefix='/user_role', tags=['user_role'])
api_router.include_router(role.router, prefix='/role', tags=['role'])
api_router.include_router(process.router, prefix='/process', tags=['process'])

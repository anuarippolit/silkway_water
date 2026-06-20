from fastapi import APIRouter, Depends
from app.schemas.user import UserResponse
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/telegram")
async def auth_tg(user: User = Depends(get_current_user)) -> UserResponse:
    return user
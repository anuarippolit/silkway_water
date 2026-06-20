from fastapi import Header, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.security import validate_telegram_init_data
from app.core.database import get_db
from app.models.user import User
import json

async def get_current_user(init_data: str = Header(...), db: AsyncSession = Depends(get_db)) -> User:
    try:
        parsed = validate_telegram_init_data(init_data)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Telegram data")
    
    user_data = json.loads(parsed["user"])
    telegram_id = user_data["id"]
    
    # ищем юзера в БД
    result = await db.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalars().first()
    
    # если не нашли — создаём
    if not user:
        user = User(
            telegram_id=telegram_id,
            name=user_data.get("first_name", ""),
            role="courier"
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    
    return user

async def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    return user
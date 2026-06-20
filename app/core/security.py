import hmac
import hashlib
from urllib.parse import parse_qsl
from app.core.config import settings

def validate_telegram_init_data(init_data: str) -> dict:
    # 1. Парсим строку в словарь
    parsed = dict(parse_qsl(init_data))
    
    # 2. Достаём hash и убираем его из данных
    received_hash = parsed.pop("hash")
    
    # 3. Сортируем оставшиеся параметры и соединяем через \n
    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(parsed.items())
    )
    
    # 4. Создаём секретный ключ
    secret_key = hmac.new(
        b"WebAppData",
        settings.BOT_TOKEN.encode(),
        hashlib.sha256
    ).digest()
    
    # 5. Подписываем данные
    calculated_hash = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256
    ).hexdigest()
    
    # 6. Сравниваем
    if calculated_hash != received_hash:
        raise ValueError("Invalid initData")
    
    return parsed
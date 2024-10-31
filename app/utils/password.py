from passlib.context import CryptContext

# Инициализация CryptContext для хеширования паролей
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # Указываем количество раундов явно
)

def hash_password(password: str) -> str:
    """Возвращает хешированный пароль"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет пароль на соответствие хешу"""
    return pwd_context.verify(plain_password, hashed_password)

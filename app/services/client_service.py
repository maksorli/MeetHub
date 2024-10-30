from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from app.models.clients import Client
from app.schemas.client_schema import ClientCreate
from pathlib import Path
from .watermark_service import  overlay_watermark
import aiofiles

AVATAR_FOLDER = Path("app/static/avatars")
WATERMARK_PATH = "app/static/watermark.png"

async def create_client_service(db: AsyncSession, client_data: dict, avatar_file):
    # Генерируем путь для аватара
    avatar_path = AVATAR_FOLDER / f"{client_data['email']}.png"
    async with aiofiles.open(avatar_path, "wb") as buffer:
        await buffer.write(await avatar_file.read())

    # Наложение водяного знака
    watermarked_avatar_path = AVATAR_FOLDER / f"watermarked_{client_data['email']}.png"
    await overlay_watermark(avatar_path, WATERMARK_PATH)

    # Создаём объект клиента
    new_client = Client(
        first_name=client_data["first_name"],
        last_name=client_data["last_name"],
        email=client_data["email"],
        gender=client_data["gender"],
        longitude=client_data["longitude"],
        latitude=client_data["latitude"],
        avatar=str(watermarked_avatar_path)
    )

    # Добавляем клиента в базу данных
    db.add(new_client)
    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        
        # Проверяем, является ли ошибка уникальности связанной с полем email
        if "ix_clients_email" in str(e.orig):
            raise ValueError("Client with this email already exists")
        else:
            raise ValueError("An error occurred while creating the client")
    
    return new_client

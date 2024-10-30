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

async def create_client_service(db: AsyncSession, client: Client, avatar_file):
    # Генерируем путь для аватара
    avatar_path = AVATAR_FOLDER / f"{client.email}.png"
    async with aiofiles.open(avatar_path, "wb") as buffer:
        await buffer.write(await avatar_file.read())

    # Наложение водяного знака
    watermarked_avatar_path = AVATAR_FOLDER / f"watermarked_{client.email}.png"
    await overlay_watermark(avatar_path, WATERMARK_PATH)

    # Обновляем путь к аватару в объекте клиента
    client.avatar = str(watermarked_avatar_path)

    # Добавляем клиента в базу данных
    db.add(client)
    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        
        # Проверяем, является ли ошибка уникальности связанной с полем email
        if "ix_clients_email" in str(e.orig):
            raise ValueError("Client with this email already exists")
        else:
            raise ValueError("An error occurred while creating the client")
    
    return client

async def get_clients(db: AsyncSession, gender: str = None, first_name: str = None, last_name: str = None, sort_by_registration: bool = False):
        query = select(Client)
        # Фильтрация
        if gender:
            query = query.where(Client.gender == gender)
        if first_name:
            query = query.where(Client.first_name.ilike(f"%{first_name}%"))
        if last_name:
            query = query.where(Client.last_name.ilike(f"%{last_name}%"))

        # Сортировка
        if sort_by_registration:
            query = query.order_by(Client.registration_date)
        else:
            query = query.order_by(Client.registration_date.desc())

        result = await db.execute(query)
        clients = result.scalars().all()
        
        return clients
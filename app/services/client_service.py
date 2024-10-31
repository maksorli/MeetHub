from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from app.models.clients import Client
from pathlib import Path
from .watermark_service import  overlay_watermark
import aiofiles
from ..utils.location import calculate_distance
from typing import List
from app.utils.password import hash_password
from app.repository.client_repository import repository_add_client,  repository_get_clients
AVATAR_FOLDER = Path("app/static/avatars")
WATERMARK_PATH = "app/static/watermark.png"

async def create_client_service(db: AsyncSession, avatar_file, client_data):
    
    
    
    client = Client(
            first_name=client_data.first_name,
            last_name=client_data.last_name,
            email=client_data.email,
            gender=client_data.gender.value,  # Используем .value для получения строкового значения
            password=hash_password(client_data.password),
            longitude=client_data.longitude,
            latitude=client_data.latitude,
    )
    
    avatar_path = AVATAR_FOLDER / f"{client.email}.png"
    async with aiofiles.open(avatar_path, "wb") as buffer:
        await buffer.write(await avatar_file.read())

    watermarked_avatar_path = AVATAR_FOLDER / f"watermarked_{client.email}.png"
    await overlay_watermark(avatar_path, WATERMARK_PATH)

    client.avatar = str(watermarked_avatar_path)

    db.add(client)
    try:
        new_client = await repository_add_client(db, client)
    except IntegrityError as e:
 
        # Обработка уникального ограничения email
        if "ix_clients_email" in str(e.orig):
            raise ValueError("Client with this email already exists")
        else:
            raise ValueError("An error occurred while creating the client")
    except Exception as e:
        await db.rollback()
        raise ValueError("An unexpected error occurred while creating the client")

    return new_client

async def get_clients(
    db: AsyncSession, 
    current_client_id: int,
    gender: str = None, 
    first_name: str = None, 
    last_name: str = None, 
    sort_by_registration: bool = False, 
    distance: int = None,  
    latitude: float = None, 
    longitude: float = None
) -> List[Client]:
    # Создаем базовый запрос к таблице Client
    clients = await repository_get_clients(
        db=db,
        current_client_id=current_client_id,
        gender=gender,
        first_name=first_name,
        last_name=last_name,
        sort_by_registration=sort_by_registration
    )

    # Применение фильтрации по расстоянию, если указан параметр `distance`
    if distance is not None and latitude is not None and longitude is not None:
        clients = [
            client for client in clients
            if calculate_distance(lat1=latitude, lon1=longitude, lat2=client.latitude, lon2=client.longitude) <= distance
        ]

    return clients
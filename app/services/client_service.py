from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from app.models.clients import Client
from pathlib import Path
from .watermark_service import  overlay_watermark
import aiofiles
from ..utils.location import calculate_distance
from typing import List

AVATAR_FOLDER = Path("app/static/avatars")
WATERMARK_PATH = "app/static/watermark.png"

async def create_client_service(db: AsyncSession, client: Client, avatar_file):
    avatar_path = AVATAR_FOLDER / f"{client.email}.png"
    async with aiofiles.open(avatar_path, "wb") as buffer:
        await buffer.write(await avatar_file.read())

    watermarked_avatar_path = AVATAR_FOLDER / f"watermarked_{client.email}.png"
    await overlay_watermark(avatar_path, WATERMARK_PATH)

    client.avatar = str(watermarked_avatar_path)

    db.add(client)
    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        
        if "ix_clients_email" in str(e.orig):
            raise ValueError("Client with this email already exists")
        else:
            raise ValueError("An error occurred while creating the client")
    
    return client

async def get_clients(
    db: AsyncSession, 
    gender: str = None, 
    first_name: str = None, 
    last_name: str = None, 
    sort_by_registration: bool = False, 
    distance: int = None,  
    latitude: float = None, 
    longitude: float = None
) -> List[Client]:
    # Создаем базовый запрос к таблице Client
    query = select(Client)
    
    # Применение фильтров по полу, имени и фамилии
    if gender:
        query = query.where(Client.gender == gender)
    if first_name:
        query = query.where(Client.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.where(Client.last_name.ilike(f"%{last_name}%"))

    # Сортировка по дате регистрации
    if sort_by_registration:
        query = query.order_by(Client.registration_date)
    else:
        query = query.order_by(Client.registration_date.desc())

    # Выполнение основного запроса
    result = await db.execute(query)
    clients = result.scalars().all()
    
    # Применение фильтрации по расстоянию, если указан параметр `distance`
    if distance is not None and latitude is not None and longitude is not None:
        clients = [
            client for client in clients
            if calculate_distance(lat1 = latitude, lon1 = longitude,lat2 =  client.latitude, lon2 = client.longitude) <= distance
        ]
        
    return clients
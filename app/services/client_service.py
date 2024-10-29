from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from app.models.clients import Client
from app.schemas.client_schema import ClientCreate

async def create_client_service(db: AsyncSession, client_data: ClientCreate):
    new_client = Client(
        first_name=client_data.first_name,
        last_name=client_data.last_name,
        email=client_data.email,
        gender=client_data.gender,
        longitude=client_data.longitude,
        latitude=client_data.latitude
    )
    
    db.add(new_client)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ValueError("Client with this email already exists")  
    return new_client

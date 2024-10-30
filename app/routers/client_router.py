from fastapi import APIRouter, Depends,UploadFile,File, Form, status, HTTPException
from typing import Annotated
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.clients import Client
from app.backend.db_depends import get_db
from app.schemas.client_schema import ClientCreate
from app.services.client_service import create_client_service

router = APIRouter(prefix='/clients', tags=['client'])


@router.get('/')
async def get_cliens(db: Annotated[AsyncSession, Depends(get_db)]):
    clients = await db.scalars(select(Client))
    return clients.all()


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_client(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    gender: str = Form(...),
    longitude: float = Form(...),
    latitude: float = Form(...),
    avatar_file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):

    client_data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "gender": gender,
        "longitude": longitude,
        "latitude": latitude,
    }
    
    try:
        # Создаем клиента через сервис
        new_client = await create_client_service(db, client_data, avatar_file)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful',
        'client': new_client
    }

@router.put('/update_client')
async def update_client():
    pass


@router.delete('/delete')
async def delete_client():
    pass
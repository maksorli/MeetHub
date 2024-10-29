from fastapi import APIRouter, Depends, status
from typing import Annotated
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.clients import Client
from app.backend.db_depends import get_db
from app.schemas.client_schema import ClientCreate
router = APIRouter(prefix='/clients', tags=['client'])


@router.get('/')
async def get_products(db: Annotated[AsyncSession, Depends(get_db)]):
    clients = await db.scalars(select(Client))
    return clients.all()


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_client(db: Annotated[AsyncSession, Depends(get_db)],
                         create_client: ClientCreate):
    await db.execute(insert(Client).values(first_name=create_client.first_name,
                                       last_name=create_client.last_name,
                                       email=create_client.email,
                                       gender=create_client.gender,
                                       longitude =create_client.longitude ,
                                       latitude = create_client.latitude))
    
                   
    await db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.put('/update_client')
async def update_client():
    pass


@router.delete('/delete')
async def delete_client():
    pass
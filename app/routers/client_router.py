from fastapi import APIRouter, Depends,UploadFile,File, Form, status, HTTPException, BackgroundTasks
from typing import Annotated
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.clients import Client
from app.backend.db_depends import get_db
from app.schemas.client_schema import ClientCreate
from app.services.client_service import create_client_service
from app.services.like_service import LikeService
router = APIRouter(prefix='/api/clients', tags=['client'])
from sqlalchemy.future import select


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
        new_client = await create_client_service(db, client_data, avatar_file)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful',
        'client': new_client
    }

@router.post("/api/clients/{id}/match")
async def like_client(
    id: int, 
    liked_id: int, 
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    like_service = LikeService(db, background_tasks)
    result, error = await like_service.record_like(id, liked_id)

    if error:
        raise HTTPException(status_code=403, detail=error)

    return {result}

 


@router.put('/update_client')
async def update_client():
    pass


@router.delete('/delete')
async def delete_client():
    pass
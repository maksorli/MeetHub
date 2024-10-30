from fastapi import APIRouter, Query, Depends,UploadFile,File, Form, status, HTTPException, BackgroundTasks
from typing import Annotated
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.clients import Client
from app.backend.db_depends import get_db
from app.schemas.client_schema import ClientCreate
from app.services.client_service import create_client_service, get_clients
from app.services.like_service import record_like
router = APIRouter(prefix='/api/clients', tags=['client'])
from sqlalchemy.future import select
from app.auth.basic_auth import get_current_user

@router.get('/')
async def get_cliens(db: Annotated[AsyncSession, Depends(get_db)]):
    clients = await db.scalars(select(Client))
    return clients.all()


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_client(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    gender: str = Form(...),
    longitude: float = Form(...),
    latitude: float = Form(...),
    avatar_file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):

    client = Client(
        first_name=first_name,
        last_name=last_name,
        email=email,
        gender=gender,
        longitude=longitude,
        latitude=latitude,
    )
    client.hash_password(password)

    try:
        new_client = await create_client_service(db, client, avatar_file)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful',
        'client': new_client
    }


@router.post("/api/clients/{id}/match")
async def like_client(
    
    liked_id: int, 
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: Client = Depends(get_current_user)
):
    result, error = await record_like(db, background_tasks, current_user.id, liked_id)
    if error:
        return {"error": error}
    return {"result": result}
 
@router.get("/api/list")
async def list_clients(
    gender: str = Query(None, description="Фильтр по полу"),
    first_name: str = Query(None, description="Фильтр по имени"),
    last_name: str = Query(None, description="Фильтр по фамилии"),
    sort_by_registration: bool = Query(False, description="Сортировка по дате регистрации (по возрастанию)"),
    db: AsyncSession = Depends(get_db),
    current_user: Client = Depends(get_current_user)
):
    clients = await get_clients(
        db=db,
        gender=gender,
        first_name=first_name,
        last_name=last_name,
        sort_by_registration=sort_by_registration
    )
    return clients

@router.put('/update_client')
async def update_client():
    pass


@router.delete('/delete')
async def delete_client():
    pass
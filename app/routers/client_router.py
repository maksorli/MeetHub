from typing import Optional

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    UploadFile,
    status,
)
from pydantic import EmailStr, ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.db_depends import get_db
from app.models.clients import Client
from app.schemas.client_schema import ClientCreate, ClientResponse, GenderEnum
from app.services.client_service import create_client_service, get_clients
from app.services.like_service import record_like

router = APIRouter(prefix="/api/clients", tags=["client"])

from app.auth.basic_auth import get_current_user


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_client(
    first_name: Optional[str] = Form(
        "Unknown", min_length=2, max_length=50, description="Имя (2-50 символов)"
    ),
    last_name: Optional[str] = Form(
        "Unknown", min_length=2, max_length=50, description="Фамилия (2-50 символов)"
    ),
    email: Optional[EmailStr] = Form(
        ..., description="Действительный адрес электронной почты"
    ),
    password: Optional[str] = Form(
        ..., min_length=8, max_length=128, description="Пароль (8-128 символов)"
    ),
    gender: Optional[GenderEnum] = Form(..., description="Пол (Male или Female)"),
    longitude: Optional[float] = Form(
        0.0, ge=-180.0, le=180.0, description="Долгота (-180 до 180)"
    ),
    latitude: Optional[float] = Form(
        0.0, ge=-90.0, le=90.0, description="Широта (-90 до 90)"
    ),
    avatar_file: Optional[UploadFile] = File(..., description="Файл аватара"),
    db: AsyncSession = Depends(get_db),
):
    # Создание экземпляра ClientCreate
    client_data = ClientCreate(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        gender=gender,
        longitude=longitude,
        latitude=latitude,
    )

    # Вызов сервиса для создания клиента
    try:
        new_client = await create_client_service(
            db, avatar_file, client_data=client_data
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return {
        "status_code": status.HTTP_201_CREATED,
        "transaction": "Successful",
        "client": ClientResponse.model_validate(new_client),
    }


@router.post("/api/clients/{id}/match")
async def like_client(
    liked_id: int,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: Client = Depends(get_current_user),
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
    sort_by_registration: bool = Query(
        False, description="Сортировка по дате регистрации (по возрастанию)"
    ),
    distance: int = Query(
        None, description="Максимальное расстояние в км от текущего пользователя"
    ),
    db: AsyncSession = Depends(get_db),
    current_user: Client = Depends(get_current_user),
):
    clients = await get_clients(
        db=db,
        current_client_id=current_user.id,
        gender=gender,
        first_name=first_name,
        last_name=last_name,
        distance=distance,
        longitude=current_user.longitude,
        latitude=current_user.latitude,
        sort_by_registration=sort_by_registration,
    )
    return clients

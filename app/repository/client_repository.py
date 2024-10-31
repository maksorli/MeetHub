from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from app.models.clients import Client
from typing import List, Optional


async def repository_add_client(db: AsyncSession, client: Client) -> Client:
        db.add(client)
        try:
            await db.commit()
        except IntegrityError as e:
            await db.rollback()
            raise e
        return client


async def repository_get_clients(
        db: AsyncSession,
        current_client_id: int,
        gender: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        sort_by_registration: bool = False
    ) -> List[Client]:
        # Создаем базовый запрос к таблице Client, исключая текущего пользователя
        query = select(Client).where(Client.id != current_client_id)
        
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

        return clients

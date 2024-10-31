from datetime import datetime

from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Client, Match
from app.services.email_service import send_email

DAILY_LIKE_LIMIT = 10


async def check_daily_limit(db: AsyncSession, liker: Client) -> bool:
    """Проверяет, достиг ли участник лимита симпатий за день"""
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    # Сброс счетчика, если прошел день
    if liker.last_like_date < today_start:
        liker.daily_likes_count = 0
        liker.last_like_date = datetime.now()
        await db.commit()

    return liker.daily_likes_count < DAILY_LIKE_LIMIT


async def record_like(
    db: AsyncSession, background_tasks: BackgroundTasks, liker_id: int, liked_id: int
):
    """Создает запись симпатии и проверяет взаимность"""
    # Получаем объекты участников
    liker = await db.get(Client, liker_id)
    liked = await db.get(Client, liked_id)

    if not liker or not liked:
        return None, "Пользователь не найден"

    # Проверка дневного лимита симпатий
    if not await check_daily_limit(db, liker):
        return None, "Достигнут лимит оценок на сегодня"

    # Проверка взаимной симпатии
    reverse_match_query = select(Match).where(
        Match.liker_id == liked_id, Match.liked_id == liker_id
    )
    reverse_match = (await db.execute(reverse_match_query)).scalar_one_or_none()

    if reverse_match:
        reverse_match.is_mutual = True
        await notify_match(liker, liked, background_tasks)

        # Обновление данных инициатора
        liker.daily_likes_count += 1
        liker.last_like_date = datetime.now()

        db.add(reverse_match)
        db.add(liker)
        await db.commit()

        return liker.email, None

    # Если симпатия не взаимная, создаем запись от liker к liked
    new_like = Match(
        liker_id=liker_id, liked_id=liked_id, timestamp=datetime.now(), is_mutual=False
    )
    db.add(new_like)
    liker.daily_likes_count += 1
    liker.last_like_date = datetime.now()
    db.add(liker)
    await db.commit()

    return "Симпатия зарегистрирована", None


async def notify_match(liker: Client, liked: Client, background_tasks: BackgroundTasks):
    """Отправляет уведомления при взаимной симпатии"""
    message_for_liker = (
        f"Вы понравились {liked.first_name}! Почта участника: {liked.email}"
    )
    message_for_liked = (
        f"Вы понравились {liker.first_name}! Почта участника: {liker.email}"
    )

    background_tasks.add_task(
        send_email, liker.email, "Взаимная симпатия", message_for_liker
    )
    background_tasks.add_task(
        send_email, liked.email, "Взаимная симпатия", message_for_liked
    )

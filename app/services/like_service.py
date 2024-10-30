
from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from app.models import Client, Match
from app.services.email_service import send_email
from sqlalchemy.future import select

DAILY_LIKE_LIMIT = 10

class LikeService:
    def __init__(self, db: AsyncSession, background_tasks: BackgroundTasks):
        self.db = db
        self.background_tasks = background_tasks

    async def check_daily_limit(self, liker: Client) -> bool:
        """Проверяет, достиг ли участник лимита симпатий за день"""
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        if liker.last_like_date < today_start:
            liker.daily_likes_count = 0
            liker.last_like_date = datetime.now()
            await self.db.commit()

        return liker.daily_likes_count < DAILY_LIKE_LIMIT



    async def record_like(self, liker_id: int, liked_id: int):
        """Создает запись симпатии и проверяет взаимность"""
        # Получаем объекты участников
        liker = await self.db.get(Client, liker_id)
        liked = await self.db.get(Client, liked_id)
        
        if not liker or not liked:
            return None, "Пользователь не найден"

        if not await self.check_daily_limit(liker):
            return None, "Достигнут лимит оценок на сегодня"

        reverse_match_query = select(Match).where(Match.liker_id == liked_id, Match.liked_id == liker_id)
        reverse_match = (await self.db.execute(reverse_match_query)).scalar_one_or_none()
        
        if reverse_match:
            reverse_match.is_mutual = True
            await self.notify_match(liker, liked)

            liker.daily_likes_count += 1
            liker.last_like_date = datetime.now()

            self.db.add(reverse_match)
            self.db.add(liker)
            await self.db.commit()
            
            return liker.email, None

        new_like = Match(liker_id=liker_id, liked_id=liked_id, timestamp=datetime.now(), is_mutual=False)
        self.db.add(new_like)
        liker.daily_likes_count += 1
        liker.last_like_date = datetime.now()
        self.db.add(liker)   
        await self.db.commit()

        return "Симпатия зарегистрирована", None
       
    async def notify_match(self, liker: Client, liked: Client):
        """Отправляет уведомления при взаимной симпатии"""
        message_for_liker = f"Вы понравились {liked.first_name}! Почта участника: {liked.email}"
        message_for_liked = f"Вы понравились {liker.first_name}! Почта участника: {liker.email}"

        self.background_tasks.add_task(send_email, liker.email, "Взаимная симпатия", message_for_liker)
        self.background_tasks.add_task(send_email, liked.email, "Взаимная симпатия", message_for_liked)
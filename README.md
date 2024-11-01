# MeetHub
MeetHub - Веб-приложение для взаимодействия участников
MeetHub — это асинхронное веб-приложение, разработанное на FastAPI для взаимодействия участников и предоставления расширенных возможностей по оценке и фильтрации профилей пользователей.


![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat&logo=python)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg?style=flat&logo=postgresql)](https://www.postgresql.org/)
![Docker](https://img.shields.io/badge/Docker-20.10-blue?style=flat&logo=docker)
![aiofiles](https://img.shields.io/badge/aiofiles-24.1.0-blue?style=flat&logo=python)
![aiosqlite](https://img.shields.io/badge/aiosqlite-0.20.0-blue?style=flat&logo=python)
![alembic](https://img.shields.io/badge/alembic-1.13.3-green?style=flat&logo=python)
![asyncpg](https://img.shields.io/badge/asyncpg-0.30.0-green?style=flat&logo=python)
![bcrypt](https://img.shields.io/badge/bcrypt-4.0.1-green?style=flat&logo=python)
![black](https://img.shields.io/badge/black-24.10.0-blue?style=flat&logo=python)
![fastapi](https://img.shields.io/badge/fastapi-0.115.4-blue?style=flat&logo=python)
![httpx](https://img.shields.io/badge/httpx-0.27.2-blue?style=flat&logo=python)
![pydantic](https://img.shields.io/badge/pydantic-2.9.2-blue?style=flat&logo=python)
![pytest](https://img.shields.io/badge/pytest-8.3.3-green?style=flat&logo=python)
![pytest-asyncio](https://img.shields.io/badge/pytest--asyncio-0.24.0-blue?style=flat&logo=python)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.36-orange?style=flat&logo=python)
![uvicorn](https://img.shields.io/badge/uvicorn-0.32.0-blue?style=flat&logo=python)


## Основные функции

### Регистрация
Возможность создания нового профиля участника с указанием основных данных, таких как имя, фамилия, адрес электронной почты, аватар, пол, геолокация (долгота и широта).
Обработка аватара с наложением водяного знака для защиты изображения профиля, реализованная асинхронно для повышения производительности.
Авторизация и безопасность

### Авторизация
Использование HTTP Basic для авторизации пользователей.
Хранение паролей в зашифрованном виде с использованием bcrypt для обеспечения безопасности.
Оценка профилей других участников

### Оценка пользователей

Участники могут оценивать профили других пользователей, что позволяет реализовать систему симпатий.
В случае взаимной симпатии приложение отправляет участникам уведомление с контактной информацией и именем понравившегося участника.
Ограничение на количество оценок

Реализована защита от злоупотребления функцией оценок — каждый пользователь имеет дневной лимит, который предотвращает спам-активность и обеспечивает комфортное взаимодействие для всех участников.
Получение списка участников с фильтрацией и сортировкой

### Фильтрация пользователей
Возможность получать список участников с фильтрацией по имени, фамилии, полу.
Сортировка участников по дате регистрации для удобства поиска новых пользователей.

Опция фильтрации списка по геолокации: возможность задать максимальную дистанцию от авторизованного пользователя, с расчетом на основе Great-circle distance.
Асинхронные технологии
MeetHub разработан с учетом высоких нагрузок и требований к производительности. Благодаря использованию асинхронных возможностей FastAPI и библиотек, таких как asyncpg, SQLAlchemy, и aiosqlite, все операции по доступу к базе данных и обработке файлов выполняются асинхронно. Это позволяет избежать блокировок и поддерживать высокую скорость отклика, даже при большом числе одновременных запросов.

### Уведомления
Уведомления через MailCatcher
Для разработки и тестирования уведомлений используется MailCatcher — удобный инструмент, который перехватывает и хранит все исходящие письма, отправленные приложением. Это позволяет разработчикам видеть и тестировать содержимое сообщений, отправляемых пользователям при взаимных симпатиях, без риска доставить их настоящим получателям.
 
 ## Установка и запуск
С использованием Docker
1. Склонируйте репозиторий:

   ```bash
   git clone https://github.com/maksorli/MeetHub.git
2. Проверьте версию Docker и Docker Compose, либо установите:
    ```bash
    docker --version
    docker-compose --version
3. Создайте файл .env  с переменными окружения (пример: .env.example)
    ```bash
        # Параметры подключения к базе данных
    POSTGRES_USER=meethub
    POSTGRES_PASSWORD=qwertyu
    POSTGRES_DB=meethub
    POSTGRES_HOST=db
    POSTGRES_PORT=5432

    # Строка подключения к базе данных
    DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
    PYTHONPATH=.
4. Запустите проект с помощью Docker Compose:
   ```bash
   docker-compose up --build
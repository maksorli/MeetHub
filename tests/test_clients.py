import pytest
from fastapi import status
from httpx import AsyncClient
from io import BytesIO
from PIL import Image

@pytest.mark.asyncio
async def test_create_client(async_client: AsyncClient):
    # Создаем временное изображение 
    img = Image.new('RGB', (100, 100), color=(73, 109, 137))
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)  # Сброс указателя в начало

    # Данные клиента для теста
    client_data = {
        "first_name": "Name1",
        "last_name": "Name2",
        "email": "test21@example.com",
        "password": "123456780",
        "gender": "Male",
        "longitude": 37.62,
        "latitude": 55.75,
    }

    # Запрос для создания клиента
    response = await async_client.post(
        "/api/clients/create",
        data=client_data,
        files={"avatar_file": ("avatar.png", img_byte_arr, "image/png")}
    )
    if response.status_code != status.HTTP_201_CREATED:
        print("Ошибка создания клиента:", response.json())  # Отладочный вывод
    # Проверка успешного создания клиента
    assert response.status_code == status.HTTP_201_CREATED
    json_response = response.json()
     
    assert json_response["transaction"] == "Successful"
    assert json_response["client"]["email"] == client_data["email"]

   


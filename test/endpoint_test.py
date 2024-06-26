from fastapi import status
from db_service.models import Meme
from db_service.shemas.shema_meme import MemeBase


async def test_api_get_memes(ac_client):
    response = await ac_client.get("/memes")
    assert response.status_code == status.HTTP_200_OK


async def test_api_get_meme(ac_client):
    response_1 = await ac_client.get("/meme/1")
    response_2 = await ac_client.get("/meme/2")
    response_3 = await ac_client.get("/meme/3")
    assert response_1.status_code == status.HTTP_200_OK
    assert response_2.status_code == status.HTTP_200_OK
    assert response_3.status_code == status.HTTP_200_OK


async def test_update_meme(ac_client, setup_database):
    # Обновляем данные мема с id=1
    update_data = {"title": "Updated Funny Cat", "description": "Updated Test Meme"}

    response = await ac_client.put("/memes/1", json=update_data)

    assert response.status_code == status.HTTP_200_OK
    updated_meme = response.json()
    assert updated_meme["title"] == "Updated Funny Cat"
    assert updated_meme["description"] == "Updated Test Meme"

    # Проверяем, что данные действительно обновились в базе данных
    response_check = await ac_client.get("/meme/1")
    assert response_check.status_code == status.HTTP_200_OK
    meme = response_check.json()
    assert meme["title"] == "Updated Funny Cat"
    assert meme["description"] == "Updated Test Meme"

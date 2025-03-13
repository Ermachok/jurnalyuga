import httpx
from fastapi import APIRouter

router = APIRouter(prefix="/word", tags=["Word of the Day"])

WORDNIK_API_KEY = "KEY"
WORDNIK_URL = "https://api.wordnik.com/v4/words.json/wordOfTheDay"


@router.get("/day")
async def get_word_of_the_day():
    async with httpx.AsyncClient() as client:
        response = await client.get(WORDNIK_URL, params={"api_key": WORDNIK_API_KEY})
        if response.status_code != 200:
            return {"error": "Не удалось получить слово дня"}

        data = response.json()
        return {
            "word": data.get("word"),
            "definition": (
                data["definitions"][0]["text"]
                if data.get("definitions")
                else "Нет определения"
            ),
        }

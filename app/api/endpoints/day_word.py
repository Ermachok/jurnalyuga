from fastapi import APIRouter, HTTPException
import httpx
import os
from dotenv import load_dotenv
from app.schemas.words import WordOfTheDayResponse

load_dotenv()

router = APIRouter(prefix="/api/wordnik", tags=["Wordnik"])

WORDNIK_API_KEY = os.getenv("WORDNIK_API_KEY")
BASE_URL = "https://api.wordnik.com/v4"

if not WORDNIK_API_KEY:
    raise ValueError("WORDNIK_API_KEY is not set in environment variables")


def remove_duplicates(seq):
    seen = set()
    result = []
    for item in seq:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


@router.get("/day_word", response_model=WordOfTheDayResponse)
async def get_word_of_the_day():
    url = f"{BASE_URL}/words.json/wordOfTheDay"
    params = {
        "api_key": WORDNIK_API_KEY
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            definitions = [d["text"] for d in data.get("definitions", [])]
            examples = [e["text"] for e in data.get("examples", [])]
            examples = remove_duplicates(examples)

            return WordOfTheDayResponse(
                word=data.get("word"),
                date=data.get("publishDate"),
                definitions=definitions,
                examples=examples
            )
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Wordnik API error: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.get("/random_word", response_model=WordOfTheDayResponse)
async def get_random_word():
    url = f"{BASE_URL}/words.json/randomWord"
    params = {
        "api_key": WORDNIK_API_KEY,
        "hasDictionaryDef": "true"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            word_data = response.json()
            word = word_data.get("word")

            definitions_url = f"{BASE_URL}/word.json/{word}/definitions"
            examples_url = f"{BASE_URL}/word.json/{word}/examples"

            definitions_resp = await client.get(definitions_url, params={"api_key": WORDNIK_API_KEY})
            examples_resp = await client.get(examples_url, params={"api_key": WORDNIK_API_KEY})

            definitions = [d["text"] for d in definitions_resp.json()]
            examples_raw = examples_resp.json().get("examples", [])
            examples = [e["text"] for e in examples_raw]
            examples = remove_duplicates(examples)

            return WordOfTheDayResponse(
                word=word,
                date=None,
                definitions=definitions,
                examples=examples
            )

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Wordnik API error: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

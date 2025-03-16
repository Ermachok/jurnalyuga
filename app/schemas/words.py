from pydantic import BaseModel
from typing import List, Optional
from dataclasses import field


class WordOfTheDayResponse(BaseModel):
    word: str
    date: str | None
    definitions: List[str]
    examples: Optional[List[str]] =  field(default_factory=list)

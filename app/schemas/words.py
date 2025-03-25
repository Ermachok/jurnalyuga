from dataclasses import field
from typing import List, Optional

from pydantic import BaseModel


class WordOfTheDayResponse(BaseModel):
    word: str
    date: str | None
    definitions: List[str]
    examples: Optional[List[str]] =  field(default_factory=list)

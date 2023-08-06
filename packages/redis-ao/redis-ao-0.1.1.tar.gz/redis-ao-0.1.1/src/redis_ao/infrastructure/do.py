from typing import Any
from pydantic import BaseModel



class RedisData(BaseModel):
    id: str
    obj: Any


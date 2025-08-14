from pydantic import BaseModel, UUID4
from typing import Optional, List


class PromptImageOut(BaseModel):
    id: int
    filename: str

    class Config:
        orm_mode = True


class PromptCreate(BaseModel):
    prompt_text: str
    description: Optional[str] = None
    is_public: bool = True


class PromptOut(BaseModel):
    id: int
    prompt_text: str
    description: Optional[str]
    is_public: bool
    share_token: str
    images: List[PromptImageOut]

    class Config:
        orm_mode = True

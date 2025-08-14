from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.prompt import Prompt, PromptImage
from app.models.user import User
from app.schemas.prompt import PromptCreate, PromptOut
from uuid import uuid4
import os
from typing import List
from fastapi import Request
from sqlalchemy.future import select
from uuid import UUID
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/prompts", tags=["Prompts"])

UPLOAD_DIR = "uploads"  # локально — можно легко заменить на облако
REAL_USER_ID = UUID("00000000-0000-0000-0000-000000007777")

os.makedirs(UPLOAD_DIR, exist_ok=True)

async def fake_current_user(db: AsyncSession = Depends(get_db)) -> User:
    result = await db.execute(select(User).where(User.id == REAL_USER_ID))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=PromptOut)
async def create_prompt(
    prompt_text: str = Form(...),
    description: str = Form(None),
    is_public: bool = Form(True),
    images: List[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(fake_current_user)  # теперь всё ок
):

    # Создаём Prompt
    prompt = Prompt(
        prompt_text=prompt_text,
        description=description,
        is_public=is_public,
        user_id=current_user.id,
        share_token=str(uuid4())
    )
    db.add(prompt)
    await db.flush()  # получить prompt.id до коммита

    # Сохраняем изображения
    if images:
        for image in images:
            filename = f"{uuid4()}_{image.filename}"
            file_path = os.path.join(UPLOAD_DIR, filename)
            with open(file_path, "wb") as f:
                f.write(await image.read())

            db.add(PromptImage(filename=filename, prompt_id=prompt.id))

    await db.commit()
    await db.refresh(prompt, attribute_names=["images"])


    return prompt

@router.get("/", response_model=List[PromptOut])
async def list_prompts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Prompt).options(selectinload(Prompt.images))
    )
    prompts = result.scalars().all()
    return prompts
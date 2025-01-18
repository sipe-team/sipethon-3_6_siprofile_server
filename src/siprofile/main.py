from fastapi import FastAPI
from src.siprofile.service.user import router as user_router
from src.siprofile.service.card import router as card_router
from src.siprofile.service.file import router as file_router

app = FastAPI()

app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(card_router, prefix="/card", tags=["card"])
app.include_router(file_router, prefix="/file", tags=["file"])

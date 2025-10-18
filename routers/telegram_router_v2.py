from fastapi import APIRouter

router = APIRouter(prefix="/telegram", tags=["telegram"])

@router.get("/webhook")
async def telegram_webhook():
    return {"message": "Telegram webhook endpoint"}


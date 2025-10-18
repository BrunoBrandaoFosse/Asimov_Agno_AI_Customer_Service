import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title="Agente de IA para Atendimento no Telegram",
    description="Agente de IA para atendimento ao cliente com Agno, Docker, RedisVL (para cache semântico)",
    version="1.0.0"
)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000)


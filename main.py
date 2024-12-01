import logging
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from app.controller.VazamentoController import router as api_router
from app.controller.UsuarioController import routerusuarios as api_router_usuarios
from app.controller.LoginController import routerlogin as api_router_login
from app.services.automacoes.TarefaVazamento import iniciar_agendador


logging.basicConfig(
    level=logging.INFO,
    filename="app.log",  # Use um caminho relativo
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Teste: configurando o logging.")

app = FastAPI()


app.include_router(api_router, prefix="/v1/api", tags=["Vazamentos"])
app.include_router(api_router_usuarios, prefix="/v1/api", tags=["Usuarios"])
app.include_router(api_router_login, prefix="/v1/api", tags=["Autenticacao"])

scheduler = AsyncIOScheduler()

@app.on_event("startup")
async def startup_event():
    global scheduler
    scheduler = iniciar_agendador()
    logging.info("Agendador iniciado junto com a API.")  # Usando logs


@app.on_event("shutdown")
async def shutdown_event():
    if scheduler:
        scheduler.shutdown()
        logging.info("Agendador encerrado com a API.")  # Usando logs


@app.get("/")
async def root():
    logging.info("Rota principal '/' acessada.")  # Log de acesso à rota principal
    return {"message": "API está rodando com agendador integrado!"}


@app.get("/hora_atual")
async def hora_atual():
    return {"hora_atual": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

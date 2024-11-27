from fastapi import FastAPI
from app.controller.VazamentoController import router as api_router

app = FastAPI()


app.include_router(api_router, prefix="/v1/api")
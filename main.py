from fastapi import FastAPI
from app.controller.VazamentoController import router as api_router
from app.controller.UsuarioController import routerusuarios as api_router_usuarios

app = FastAPI()


app.include_router(api_router, prefix="/v1/api")
app.include_router(api_router_usuarios, prefix="/v1/api")
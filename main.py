from fastapi import FastAPI
from app.controller.VazamentoController import router as api_router
from app.controller.UsuarioController import routerusuarios as api_router_usuarios
from app.controller.LoginController import routerlogin as api_router_login

app = FastAPI()


app.include_router(api_router, prefix="/v1/api", tags=["Vazamentos"])
app.include_router(api_router_usuarios, prefix="/v1/api", tags=["Usuarios"])
app.include_router(api_router_login, prefix="/v1/api", tags=["Autenticacao"])
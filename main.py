from fastapi import FastAPI

# Importa todos os módulos de endpoints
from app.api.endpoints import upload, history, search, reset

# Cria a aplicação FastAPI
app = FastAPI(title="API do Desafio")

# Inclui os routers registrados
app.include_router(upload.router)
app.include_router(history.router)
app.include_router(search.router)
app.include_router(reset.router)  # 🔧 Inclua este para ativar o endpoint /reset

# Rota raiz apenas para verificação
@app.get("/")
def read_root():
    return {"message": "API do desafio funcionando!"}

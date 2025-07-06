# app/api/reset.py

from fastapi import APIRouter
from app.services.data_store import data_store

router = APIRouter()

@router.post("/reset", tags=["Admin"])
async def reset_data():
    """
    Limpa os dados carregados em memória:
    - Arquivos enviados
    - Dados carregados
    - Histórico de uploads
    """
    data_store.uploaded_data = []
    data_store.uploaded_files.clear()
    data_store.uploaded_files_info.clear()

    return {"message": "Dados resetados com sucesso."}

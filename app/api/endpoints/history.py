from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.services.data_store import data_store

# Cria o roteador para os endpoints de histórico
router = APIRouter()

@router.get("/upload-history")
def get_upload_history(
    filename: Optional[str] = Query(None, description="Nome do arquivo"),
    reference_date: Optional[str] = Query(None, description="Data de referência no formato YYYY-MM-DD")
):
    """
    Retorna o histórico de uploads realizados.
    Permite buscar por nome do arquivo (filename) e/ou data de referência (reference_date).
    Se nenhum filtro for fornecido, retorna todos os uploads.
    """

    uploads = data_store.uploaded_files_info

    if not filename and not reference_date:
        return uploads  # Sem filtros, retorna tudo

    # Aplica os filtros cumulativos (se ambos forem fornecidos, ambos devem bater)
    filtered = []
    for info in uploads:
        match = True
        if filename and info["nome_arquivo"] != filename:
            match = False
        if reference_date and info["data_referencia"] != reference_date:
            match = False
        if match:
            filtered.append(info)

    if not filtered:
        raise HTTPException(status_code=404, detail="Nenhum upload encontrado com os filtros fornecidos.")

    return filtered

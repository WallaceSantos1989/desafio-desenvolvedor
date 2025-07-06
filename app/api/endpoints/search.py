from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from datetime import datetime
from app.services.data_store import data_store  # Acesso ao armazenamento de dados
import math

router = APIRouter()

def normalize_date(value: str) -> Optional[str]:
    """
    Converte datas em diferentes formatos (ex: 'DD/MM/YYYY') para o padrão ISO 'YYYY-MM-DD'.
    Retorna None se não for possível converter.
    """
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(value.strip(), fmt).date().isoformat()
        except Exception:
            continue
    return None

def json_safe(obj):
    """
    Converte recursivamente valores NaN, inf e -inf em None, para evitar erros na serialização JSON.
    """
    if isinstance(obj, dict):
        return {k: json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [json_safe(v) for v in obj]
    elif isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
        return None
    else:
        return obj

@router.get("/search")
async def search_data(
    RptDt: Optional[str] = Query(None, description="Data do relatório (YYYY-MM-DD ou DD/MM/YYYY)"),
    TckrSymb: Optional[str] = Query(None, description="Ticker do ativo"),
    page: int = Query(1, ge=1, description="Página (mínimo 1)"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página (1-100)")
):
    # Verifica se há dados carregados
    if not data_store.uploaded_data:
        raise HTTPException(status_code=400, detail="Nenhum dado carregado. Faça upload primeiro.")

    registros = data_store.uploaded_data

    # Normaliza a data de entrada, se fornecida
    filtro_rptdt = normalize_date(RptDt) if RptDt else None
    if RptDt and filtro_rptdt is None:
        raise HTTPException(status_code=400, detail="Formato inválido para o parâmetro RptDt.")

    # Normaliza o ticker de entrada, se fornecido
    filtro_tckr = TckrSymb.strip().casefold() if TckrSymb else None

    filtrado = []

    # Aplica os filtros nos dados carregados
    for item in registros:
        item_rptdt = normalize_date(str(item.get("RptDt", "")))
        item_tckr = str(item.get("TckrSymb", "")).strip().casefold()

        # Combina os filtros conforme fornecido
        if filtro_rptdt and filtro_tckr:
            if item_rptdt == filtro_rptdt and item_tckr == filtro_tckr:
                filtrado.append(item)
        elif filtro_rptdt:
            if item_rptdt == filtro_rptdt:
                filtrado.append(item)
        elif filtro_tckr:
            if item_tckr == filtro_tckr:
                filtrado.append(item)
        else:
            # Sem filtros: retorna todos os registros
            filtrado.append(item)

    # Retorna erro se nenhum dado foi encontrado com os filtros
    if not filtrado:
        raise HTTPException(status_code=404, detail="Nenhum dado encontrado para os filtros informados.")

    # Paginação dos resultados
    start = (page - 1) * page_size
    end = start + page_size

    # Retorna os dados paginados com tratamento para valores não serializáveis
    return {
        "page": page,
        "page_size": page_size,
        "total": len(filtrado),
        "results": json_safe(filtrado[start:end])  # Garante compatibilidade com JSON (ex: trata NaN)
    }

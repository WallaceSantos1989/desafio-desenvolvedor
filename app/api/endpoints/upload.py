from fastapi import APIRouter, UploadFile, File, HTTPException
from datetime import datetime
from typing import Optional
import pandas as pd
import re

# Importa o objeto de armazenamento em memória
from app.services.data_store import data_store

# Instancia o router da FastAPI
router = APIRouter()

# Função auxiliar para extrair data de referência do nome do arquivo
def extract_reference_date(filename: str) -> Optional[str]:
    """
    Extrai uma data no formato 'YYYYMMDD' do nome do arquivo e converte para 'YYYY-MM-DD'.
    """
    match = re.search(r'(\d{8})', filename)
    if match:
        date_str = match.group(1)
        return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
    return None

# Função para armazenar os dados carregados no data_store
def load_data(df: pd.DataFrame):
    """
    Converte o DataFrame em uma lista de dicionários e armazena em memória.
    """
    data_store.uploaded_data = df.to_dict(orient="records")

# Endpoint de upload
@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Recebe um arquivo CSV ou Excel, processa e armazena os dados em memória.
    Também registra informações sobre o arquivo e realiza normalizações essenciais.
    """
    filename = file.filename

    # Verifica se o arquivo já foi enviado antes
    if filename in data_store.uploaded_files:
        raise HTTPException(status_code=400, detail="Arquivo já enviado.")

    # Aceita apenas arquivos .csv ou .xlsx
    if not (filename.endswith(".csv") or filename.endswith(".xlsx")):
        raise HTTPException(status_code=400, detail="Formato inválido. Envie .csv ou .xlsx.")

    try:
        # Lê o arquivo de acordo com o tipo (CSV ou Excel)
        if filename.endswith(".csv"):
            df = pd.read_csv(file.file, encoding='latin1', delimiter=';', header=0)
        else:
            df = pd.read_excel(file.file)

        # Remove espaços dos nomes das colunas
        df.columns = df.columns.str.strip()

        # Normaliza a coluna 'RptDt', se existir
        if "RptDt" in df.columns:
            df["RptDt"] = pd.to_datetime(df["RptDt"], dayfirst=True, errors="coerce")
            df["RptDt"] = df["RptDt"].dt.strftime('%Y-%m-%d')  # Converte para string no formato ISO

        # Normaliza a coluna 'TckrSymb' (ticker), se existir
        if "TckrSymb" in df.columns:
            df["TckrSymb"] = df["TckrSymb"].astype(str).str.strip().str.upper()

        # Armazena o nome do arquivo como já enviado
        data_store.uploaded_files.add(filename)

        # Extrai data de referência do nome do arquivo (ex: 20250704 -> 2025-07-04)
        reference_date = extract_reference_date(filename)

        # Registra informações sobre o upload
        data_store.uploaded_files_info.append({
            "nome_arquivo": filename,
            "data_upload": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data_referencia": reference_date
        })

        # Carrega os dados para a memória
        load_data(df)

        # Resposta de sucesso com informações úteis
        return {
            "message": f"Arquivo '{filename}' recebido com sucesso.",
            "linhas": len(df),
            "colunas": list(df.columns)  # Útil para debug
        }

    except Exception as e:
        # Retorna erro genérico com mensagem da exceção
        raise HTTPException(status_code=500, detail=f"Erro ao processar o arquivo: {str(e)}")

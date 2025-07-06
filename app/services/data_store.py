# Este módulo atua como memória em tempo de execução da aplicação.
# Serve para armazenar dados entre diferentes chamadas de endpoints.

from typing import List, Dict, Set

class DataStore:
    def __init__(self):
        # Lista de registros carregados do arquivo, cada um como dicionário (ex: {"RptDt": "2023-01-01", "TckrSymb": "VALE3"})
        self.uploaded_data: List[Dict] = []

        # Conjunto com os nomes dos arquivos enviados (usado para evitar duplicidade)
        self.uploaded_files: Set[str] = set()

        # Lista de metadados sobre uploads realizados (nome do arquivo, data de upload, data de referência)
        self.uploaded_files_info: List[Dict] = []

# Instância global acessada por todos os módulos
data_store = DataStore()

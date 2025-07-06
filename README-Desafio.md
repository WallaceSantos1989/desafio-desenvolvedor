
# Desafio de Desenvolvedor – Oliveira Trust

Este repositório contém a solução do desafio proposto pela **Oliveira Trust** para a vaga de Desenvolvedor. A proposta foi desenvolvida em **Python**, utilizando **VS Code** e terminal **PowerShell**.

---

## 🧠 Objetivo do Desafio

O objetivo principal é avaliar a capacidade de aplicar regras de negócio, estruturar código limpo e organizado e criar uma API funcional com os seguintes recursos:

- ✅ Upload de arquivos `.csv` ou `.xlsx`
- ✅ Histórico de uploads
- ✅ Busca por dados com filtros opcionais

---

## 🚀 Tecnologias Utilizadas

- **Python 3.10+**
- **FastAPI**
- **Pandas**
- **Uvicorn**
- **VS Code**
- **PowerShell (ambiente Windows)**


## 📦 Como rodar o projeto localmente

### 1. Clone o repositório

```bash
git clone https://github.com/WallaceSantos1989/desafio-desenvolvedor.git
cd desafio-desenvolvedor
git checkout Wallace-Euzebio-dos-Santos
```

### 2. Crie o ambiente virtual

```bash
python -m venv venv
```

### 3. Ative o ambiente

No Windows PowerShell:

```bash
.env\Scripts\Activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Rode o servidor local

```bash
uvicorn app.main:app --reload
```

Acesse em: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📡 Endpoints da API

### `POST /upload`
- Faz o upload de um arquivo `.csv` ou `.xlsx`
- Rejeita arquivos duplicados (mesmo nome)

### `GET /uploads`
- Lista o histórico de uploads
- Filtros opcionais: `nome_do_arquivo`, `data_referencia`

### `GET /buscar`
- Busca dados com base nos parâmetros:
  - `TckrSymb`
  - `RptDt`
- Se não forem informados, os resultados são paginados

### 🧾 Exemplo de resposta:

```json
{
  "RptDt": "2024-08-22",
  "TckrSymb": "AMZO34",
  "MktNm": "EQUITY-CASH",
  "SctyCtgyNm": "BDR",
  "ISIN": "BRAMZOBDR002",
  "CrpnNm": "AMAZON.COM, INC"
}
```

---

## 🔎 Regras de Negócio Implementadas

- Não é permitido o reenvio de arquivos com o mesmo nome.
- Permite busca por nome do arquivo ou data de referência.
- Permite busca de dados por `TckrSymb` e `RptDt` com paginação.
- Lê e processa grandes volumes de dados (75.000+ linhas) com eficiência.

---

## 📬 Contato

- LinkedIn: https://www.linkedin.com/in/wallaceeuzebiodossantos/
- GitHub: https://github.com/WallaceSantos1989
- Email: wave5314@gmail.com

---

> Obrigado pela oportunidade! Estou à disposição para qualquer dúvida.

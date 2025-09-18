"""Configurações centralizadas do projeto"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Diretórios
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
STORAGE_DIR = BASE_DIR / "storage"

# Criar diretórios se não existirem
DATA_DIR.mkdir(exist_ok=True)
STORAGE_DIR.mkdir(exist_ok=True)

# Configurações de API
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
TODOIST_API_KEY = os.getenv("TODOIST_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# URLs base
TODOIST_BASE_URL = "https://api.todoist.com/rest/v2"

# Headers padrão para Todoist
TODOIST_HEADERS = {
    "Authorization": f"Bearer {TODOIST_API_KEY}",
    "Content-Type": "application/json"
} if TODOIST_API_KEY else {}

# Configurações do AgentOS
AGENTOS_DEFAULT_PORT = 7777
AGENTOS_DEFAULT_HOST = "localhost"

# Configurações de modelo padrão
DEFAULT_MODEL = "openai/gpt-4o-mini"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 2000
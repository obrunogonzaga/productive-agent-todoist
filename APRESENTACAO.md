# 🎯 Script de Apresentação - Workshop Assistentes Produtivos

## 📋 Preparação Inicial
```bash
# Instalar o UV (gerenciador de pacotes moderno Python)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Inicializar projeto
uv init productive-agents
cd productive-agents

# Criar ambiente virtual
uv venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate    # Windows

# Instalar AgentOS
uv add agno python-dotenv openai requests
```

---

## Módulo 1: Primeiros Passos com LLMs
### 🎤 **Introdução (5 min)**
"Hoje vamos construir assistentes inteligentes que realmente ajudam no dia a dia. Começaremos do básico até recursos avançados como memória persistente."

### 📝 **Hands-on: Chamando LLMs (10 min)**

**1. Criar arquivo `.env`:**
```env
OPENROUTER_API_KEY=seu_api_key_aqui
TODOIST_API_KEY=seu_todoist_api_key_aqui
```

**2. Criar `1-calling-llm.py`:**
```python
"""Nosso primeiro contato com LLMs via AgentOS"""
from agno.models.openrouter import OpenRouter
from dotenv import load_dotenv
import os

load_dotenv()

# Inicializar o modelo
model = OpenRouter(
    id="openai/gpt-4o-mini",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# Fazer uma pergunta simples
response = model.run(
    messages=[
        {"role": "user", "content": "O que é Python em 2 frases?"}
    ]
)

print(response.content)
```

### 💡 **Conceitos-chave:**
- OpenRouter como gateway para múltiplos modelos
- Configuração segura via variáveis de ambiente
- Estrutura básica de mensagens (role/content)

---

## Módulo 2: Criando Nosso Primeiro Agente
### 🎤 **Transição (2 min)**
"LLMs são poderosos, mas agentes são LLMs com superpoderes. Podem usar ferramentas, manter contexto e executar ações."

### 📝 **Hands-on: Agente Pesquisador (15 min)**

**1. Instalar ferramenta de pesquisa:**
```bash
uv add tavily-python
```

**2. Criar `2-researcher-agent.py`:**
```python
"""Agente pesquisador - nosso primeiro agente com ferramentas"""
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.tools.tavily import TavilyTools
from dotenv import load_dotenv
import os

load_dotenv()

# Criar agente pesquisador
researcher = Agent(
    name="Pesquisador Web",
    instructions="""Você é um pesquisador especializado.
    Use a ferramenta de busca para encontrar informações atualizadas.
    Sempre cite suas fontes.""",
    tools=[TavilyTools()],  # Ferramenta de pesquisa web
    model=OpenRouter(
        id="openai/gpt-4o-mini",
        api_key=os.getenv("OPENROUTER_API_KEY")
    ),
    markdown=True
)

# Testar o agente
response = researcher.run("Quais são as últimas novidades sobre IA em 2024?")
print(response.content)
```

### 💡 **Conceitos-chave:**
- Agentes vs LLMs puros
- Conceito de Tools (menção OpenAI e Anthropic)
- Instructions como "personalidade" do agente
- Importância da estrutura modular (agno.tools.tavily)

---

## Módulo 3: Agente com Ferramentas Customizadas
### 🎤 **Transição (2 min)**
"Agora vamos criar ferramentas próprias. Nosso agente vai gerenciar tarefas reais no Todoist."

### 📝 **Hands-on: Integrando com Todoist (20 min)**

**Criar `3-todoist-tools.py`:**
```python
"""Ferramentas customizadas para Todoist"""
from agno.tools import tool
import requests
import os
from datetime import datetime

TODOIST_API_KEY = os.getenv("TODOIST_API_KEY")
HEADERS = {
    "Authorization": f"Bearer {TODOIST_API_KEY}",
    "Content-Type": "application/json"
}

@tool
def list_todoist_tasks(filter: str = None) -> str:
    """
    Lista tarefas do Todoist.
    Args:
        filter: 'hoje', 'amanhã', 'semana' ou None para todas
    """
    # Implementação simplificada
    response = requests.get(
        "https://api.todoist.com/rest/v2/tasks",
        headers=HEADERS
    )
    
    if response.status_code == 200:
        tasks = response.json()
        if not tasks:
            return "Nenhuma tarefa encontrada"
        
        result = "📋 Suas tarefas:\n"
        for task in tasks[:5]:  # Limitar para demo
            result += f"- [{task['id']}] {task['content']}\n"
        return result
    return f"Erro: {response.status_code}"

@tool
def add_todoist_task(content: str, due_date: str = None) -> str:
    """Adiciona nova tarefa ao Todoist"""
    data = {"content": content}
    if due_date:
        data["due_date"] = due_date
    
    response = requests.post(
        "https://api.todoist.com/rest/v2/tasks",
        headers=HEADERS,
        json=data
    )
    
    if response.status_code == 200:
        return f"✅ Tarefa '{content}' adicionada!"
    return f"Erro ao adicionar tarefa"
```

### 💡 **Conceitos-chave:**
- Decorator `@tool` transforma função em ferramenta
- Docstrings são críticas (o agente lê!)
- Type hints ajudam o agente
- Retornos estruturados e claros

---

## Módulo 4: Agente Completo com Interface
### 🎤 **Transição (2 min)**
"Vamos juntar tudo: agente, ferramentas e uma interface web profissional."

### 📝 **Hands-on: Assistente Todoist (15 min)**

**Criar `4-todoist-assistant.py`:**
```python
"""Assistente completo com interface web"""
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.tools import tool
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# [Incluir as ferramentas do módulo anterior]

# Criar agente assistente
assistant = Agent(
    name="Assistente Todoist",
    instructions="""Você é um assistente de produtividade.
    Ajude o usuário a gerenciar suas tarefas no Todoist.
    Seja proativo e sugira organizações.""",
    tools=[list_todoist_tasks, add_todoist_task],
    model=OpenRouter(
        id="openai/gpt-4o-mini",
        api_key=os.getenv("OPENROUTER_API_KEY")
    ),
    markdown=True
)

# Modo interativo
print("🤖 Assistente Todoist iniciado!")
print("Digite 'sair' para encerrar\n")

while True:
    user_input = input("Você: ")
    if user_input.lower() == 'sair':
        break
    
    response = assistant.run(user_input)
    print(f"\nAssistente: {response.content}\n")
```

---

## Módulo 5: AgentOS - Interface Profissional
### 🎤 **Transição (3 min)**
"AgentOS transforma nosso agente em uma aplicação completa com API REST, interface web e muito mais."

### 📝 **Hands-on: Deploy com AgentOS (15 min)**

**Criar `5-assistente-agentos.py`:**
```python
"""Assistente com AgentOS - produção ready"""
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.os import AgentOS
from agno.os.interfaces.agui import AGUI
# [Importar ferramentas]

# Criar agente
agent = Agent(
    name="Assistente Todoist",
    instructions="...",
    tools=[...],
    model=OpenRouter(...),
    add_history_to_context=True,  # Mantém contexto
    num_history_runs=5,
    markdown=True
)

# Criar AgentOS
agent_os = AgentOS(
    os_id="todoist-assistant-v1",
    description="Assistente de produtividade",
    agents=[agent],
    interfaces=[AGUI(agent=agent)],  # Interface web automática!
    telemetry=True,  # Analytics
    enable_mcp=True,  # MCP server para integrações
)

# Obter app FastAPI
app = agent_os.get_app()

if __name__ == "__main__":
    print("🚀 Iniciando em http://localhost:7777")
    agent_os.serve(app="5-assistente-agentos:app", port=7777)
```

### 💡 **Conceitos-chave:**
- AgentOS como framework de produção
- AGUI gera interface automaticamente
- API REST incluída (`/docs` para Swagger)
- Telemetria para monitoramento

---

## Módulo 6: Storage Persistente
### 🎤 **Transição (2 min)**
"Nossos agentes perdem memória ao reiniciar. Vamos adicionar storage persistente."

### 📝 **Hands-on: SQLite Storage (10 min)**

**Modificar para `6-storage.py`:**
```python
from agno.storage import SqliteStorage

# Adicionar storage ao agente
agent = Agent(
    # ... configurações anteriores ...
    storage=SqliteStorage(
        db_file="storage/assistant.db",
        table_name="interactions"
    )
)

# AgentOS também com storage
agent_os = AgentOS(
    # ... configurações anteriores ...
    storage=SqliteStorage(
        db_file="storage/agentos.db",
        table_name="agentos_data"
    )
)
```

### 💡 **Conceitos-chave:**
- Persistência entre sessões
- Histórico de interações
- Backup automático
- Recuperação de contexto

---

## Módulo 7: Memória Contextual
### 🎤 **Transição (2 min)**
"Storage guarda dados. Memória permite que o agente lembre e use informações de forma inteligente."

### 📝 **Hands-on: Sistema de Memória (15 min)**

**Criar ferramentas de memória:**
```python
@tool
def remember_preference(key: str, value: str) -> str:
    """Armazena preferência do usuário"""
    memory_manager.remember(key, value)
    return f"✅ Vou lembrar que {key}: {value}"

@tool
def recall_preference(key: str) -> str:
    """Recupera preferência armazenada"""
    value = memory_manager.recall(key)
    if value:
        return f"📝 Lembro que {key}: {value}"
    return f"Não tenho informação sobre {key}"
```

### 💡 **Conceitos-chave:**
- Memória vs Storage
- Contexto personalizado
- Preferências do usuário
- Aprendizado contínuo

---

## Módulo 8: MCP Server - Integrações
### 🎤 **Transição (2 min)**
"MCP (Model Context Protocol) permite que nosso agente seja usado em qualquer lugar: VSCode, CLIs, outros apps."

### 📝 **Demonstração: MCP em Ação (10 min)**

**Configuração MCP:**
```json
{
  "mcpServers": {
    "todoist-assistant": {
      "url": "http://localhost:7777/mcp",
      "transport": "http"
    }
  }
}
```

**Testar via curl:**
```bash
curl -X POST "http://localhost:7777/agent/run" \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "assistant", "input": "Liste tarefas de hoje"}'
```

### 💡 **Conceitos-chave:**
- Protocolo padronizado Anthropic
- Integração com IDEs
- APIs unificadas
- Ecosistema de ferramentas

---

## Módulo 9: Multi-Agentes e Teams
### 🎤 **Gran Finale (5 min)**
"Agentes podem trabalhar em equipe. Cada um especializado em sua área."

### 📝 **Demo: Time de Agentes (10 min)**

```python
# Criar time de agentes
team = Team(
    agents=[
        researcher_agent,    # Pesquisa informações
        writer_agent,       # Escreve conteúdo
        reviewer_agent,     # Revisa e melhora
    ],
    workflow="sequential"  # Ou "parallel", "hierarchical"
)

result = team.run("Crie um artigo sobre IA")
```

---

## 📊 Resumo e Q&A (10 min)

### Recapitulando o que construímos:
1. ✅ LLM básico → Agente com ferramentas
2. ✅ Ferramentas customizadas (Todoist)
3. ✅ Interface profissional (AgentOS)
4. ✅ Storage e Memória persistente
5. ✅ Integrações via MCP
6. ✅ Times de agentes

### Próximos passos:
- Experimentar com diferentes modelos
- Criar ferramentas para seu workflow
- Integrar com suas ferramentas favoritas
- Explorar RAG e embeddings

### Recursos:
- Repo: github.com/seu-usuario/productive-agents
- Docs AgentOS: docs.agno.dev
- MCP Protocol: modelcontextprotocol.io

---

## 🎁 Bonus: Dicas de Produção

### Performance:
```python
# Cache de respostas
agent.enable_caching = True

# Rate limiting
agent.max_requests_per_minute = 60

# Timeout handling
agent.request_timeout = 30
```

### Segurança:
```python
# Validação de inputs
@tool
def safe_task_add(content: str):
    if len(content) > 500:
        return "Tarefa muito longa"
    # sanitizar input
    content = sanitize(content)
    return add_task(content)
```

### Monitoramento:
```python
# Logs estruturados
import logging
logging.basicConfig(level=logging.INFO)

# Métricas
from agno.telemetry import track_event
track_event("task_added", {"user_id": "123"})
```

---

**"Construam assistentes que resolvem problemas reais!"** 🚀
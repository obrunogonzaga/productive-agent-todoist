"""Assistente Todoist com armazenamento persistente"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.os import AgentOS
from agno.os.interfaces.agui import AGUI
from agno.storage import SqliteStorage
from src.config import OPENROUTER_API_KEY, DEFAULT_MODEL, AGENTOS_DEFAULT_PORT
from src.tools import (
    list_todoist_tasks,
    add_todoist_task,
    complete_todoist_task,
    list_completed_tasks
)


def create_todoist_assistant_with_storage():
    """Cria o assistente Todoist com armazenamento persistente."""
    agent = Agent(
        name="Assistente Todoist com Storage",
        instructions="""Você é um assistente especializado em gerenciar tarefas no Todoist.
        
        Você pode:
        - Listar tarefas (todas, hoje, amanhã, semana, vencidas)
        - Adicionar novas tarefas com datas
        - Marcar tarefas como concluídas
        - Mostrar tarefas já concluídas
        
        Importante: Você tem armazenamento persistente e mantém histórico das interações.
        Seja sempre claro e organizado nas respostas.""",
        tools=[
            list_todoist_tasks,
            add_todoist_task,
            complete_todoist_task,
            list_completed_tasks
        ],
        model=OpenRouter(
            id=DEFAULT_MODEL,
            api_key=OPENROUTER_API_KEY
        ),
        add_history_to_context=True,
        num_history_runs=10,  # Mais histórico com storage
        markdown=True,
        storage=SqliteStorage(
            db_file="storage/todoist_assistant.db",
            table_name="interactions"
        )
    )
    
    return agent


def main():
    """Função principal para executar o assistente com storage."""
    # Criar o agente
    agent = create_todoist_assistant_with_storage()
    
    # Criar o AgentOS
    agent_os = AgentOS(
        os_id="todoist-assistant-storage-v1",
        description="Assistente Todoist com armazenamento persistente",
        agents=[agent],
        interfaces=[AGUI(agent=agent)],
        telemetry=True,
        enable_mcp=True,
        storage=SqliteStorage(
            db_file="storage/agentos_storage.db",
            table_name="agentos_data"
        )
    )
    
    # Obter a aplicação FastAPI
    app = agent_os.get_app()
    
    print("╔══════════════════════════════════════════════════════╗")
    print("║   🤖 Assistente Todoist com Storage Persistente     ║")
    print("╚══════════════════════════════════════════════════════╝")
    print()
    print("📍 Endpoints disponíveis:")
    print(f"  • http://localhost:{AGENTOS_DEFAULT_PORT}/docs    - Documentação da API")
    print(f"  • http://localhost:{AGENTOS_DEFAULT_PORT}/config  - Configuração do AgentOS")
    print(f"  • http://localhost:{AGENTOS_DEFAULT_PORT}/storage - Visualizar dados armazenados")
    print(f"  • http://localhost:{AGENTOS_DEFAULT_PORT}/history - Histórico de interações")
    print(f"  • http://localhost:{AGENTOS_DEFAULT_PORT}/mcp     - MCP Server endpoint")
    print()
    print("💾 Recursos de Armazenamento:")
    print("  • Histórico persistente de conversas")
    print("  • Backup automático de dados")
    print("  • Recuperação de contexto entre sessões")
    print()
    print("💡 Exemplos de comandos:")
    print("  • Liste minhas tarefas")
    print("  • Adicione tarefa: Revisar código às 15h")
    print("  • Mostre o que fizemos ontem")
    print("  • Complete a tarefa [ID]")
    print()
    print("🚀 Iniciando servidor com storage...")
    print()
    
    agent_os.serve(
        app="src.assistants.todoist_with_storage:app",
        port=AGENTOS_DEFAULT_PORT
    )


# Criar app para importação
agent = create_todoist_assistant_with_storage()
agent_os = AgentOS(
    os_id="todoist-assistant-storage-v1",
    description="Assistente Todoist com armazenamento persistente",
    agents=[agent],
    interfaces=[AGUI(agent=agent)],
    telemetry=True,
    enable_mcp=True,
    storage=SqliteStorage(
        db_file="storage/agentos_storage.db",
        table_name="agentos_data"
    )
)
app = agent_os.get_app()


if __name__ == "__main__":
    main()
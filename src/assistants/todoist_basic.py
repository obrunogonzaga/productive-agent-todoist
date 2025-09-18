"""Assistente Todoist básico com AgentOS"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.os import AgentOS
from agno.os.interfaces.agui import AGUI
from src.config import OPENROUTER_API_KEY, DEFAULT_MODEL, AGENTOS_DEFAULT_PORT
from src.tools import (
    list_todoist_tasks,
    add_todoist_task,
    complete_todoist_task,
    list_completed_tasks
)


def create_todoist_assistant():
    """Cria o assistente Todoist básico."""
    agent = Agent(
        name="Assistente Todoist",
        instructions="""Você é um assistente especializado em gerenciar tarefas no Todoist.
        
        Você pode:
        - Listar tarefas (todas, hoje, amanhã, semana, vencidas)
        - Adicionar novas tarefas com datas
        - Marcar tarefas como concluídas
        - Mostrar tarefas já concluídas
        
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
        num_history_runs=5,
        markdown=True
    )
    
    return agent


def main():
    """Função principal para executar o assistente."""
    # Criar o agente
    agent = create_todoist_assistant()
    
    # Criar o AgentOS
    agent_os = AgentOS(
        os_id="todoist-assistant-v1",
        description="Assistente Todoist com gerenciamento completo de tarefas",
        agents=[agent],
        interfaces=[AGUI(agent=agent)],
        telemetry=True,
        enable_mcp=True,  # MCP server habilitado para integrações
    )
    
    # Obter a aplicação FastAPI
    app = agent_os.get_app()
    
    print("╔══════════════════════════════════════════════════════╗")
    print("║       🤖 Assistente Todoist com AgentOS             ║")
    print("╚══════════════════════════════════════════════════════╝")
    print()
    print("📍 Endpoints disponíveis:")
    print(f"  • http://localhost:{AGENTOS_DEFAULT_PORT}/docs    - Documentação da API")
    print(f"  • http://localhost:{AGENTOS_DEFAULT_PORT}/config  - Configuração do AgentOS")
    print(f"  • http://localhost:{AGENTOS_DEFAULT_PORT}/agents  - Listar agentes")
    print(f"  • http://localhost:{AGENTOS_DEFAULT_PORT}/runs    - Histórico de execuções")
    print(f"  • http://localhost:{AGENTOS_DEFAULT_PORT}/mcp     - MCP Server endpoint")
    print()
    print("🎯 Para usar o agente via API:")
    print(f'  curl -X POST "http://localhost:{AGENTOS_DEFAULT_PORT}/agent/run" \\')
    print('       -H "Content-Type: application/json" \\')
    print('       -d \'{"agent_id": "assistente-todoist", "input": "Liste minhas tarefas"}\'')
    print()
    print("💡 Exemplos de comandos:")
    print("  • Liste minhas tarefas")
    print("  • Liste as tarefas de hoje")
    print("  • Adicione tarefa: Estudar Python amanhã")
    print("  • Complete a tarefa [ID]")
    print()
    print("🚀 Iniciando servidor...")
    print()
    
    # Serve sem reload quando usando MCP
    agent_os.serve(
        app="src.assistants.todoist_basic:app",
        port=AGENTOS_DEFAULT_PORT
    )


# Criar app para importação
agent = create_todoist_assistant()
agent_os = AgentOS(
    os_id="todoist-assistant-v1",
    description="Assistente Todoist com gerenciamento completo de tarefas",
    agents=[agent],
    interfaces=[AGUI(agent=agent)],
    telemetry=True,
    enable_mcp=True,
)
app = agent_os.get_app()


if __name__ == "__main__":
    main()
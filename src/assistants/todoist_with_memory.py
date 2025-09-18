"""Assistente Todoist com memória persistente avançada"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.tools import tool
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
from src.utils import MemoryManager


# Inicializar o gerenciador de memória
memory_manager = MemoryManager()


@tool
def remember_preference(key: str, value: str) -> str:
    """
    Armazena uma preferência ou informação do usuário na memória.
    
    Args:
        key: Chave da preferência (ex: "projeto_prioritário", "horário_preferido")
        value: Valor da preferência
    """
    memory_manager.remember(key, value)
    return f"✅ Vou lembrar que {key}: {value}"


@tool
def recall_preference(key: str) -> str:
    """
    Recupera uma preferência ou informação armazenada na memória.
    
    Args:
        key: Chave da preferência a recuperar
    """
    value = memory_manager.recall(key)
    if value:
        return f"📝 Lembro que {key}: {value}"
    return f"❌ Não tenho informação sobre '{key}' na memória"


@tool
def show_all_memories() -> str:
    """Mostra todas as preferências e informações armazenadas na memória."""
    memories = memory_manager.get_all_memories()
    if not memories:
        return "📭 Ainda não tenho nenhuma memória armazenada"
    
    result = "🧠 Minhas memórias sobre você:\n"
    for key, data in memories.items():
        value = data.get("value", "")
        result += f"  • {key}: {value}\n"
    
    return result


@tool
def clear_all_memories() -> str:
    """Limpa todas as memórias armazenadas."""
    memory_manager.clear_memories()
    return "🧹 Todas as memórias foram limpas"


def create_todoist_assistant_with_memory():
    """Cria o assistente Todoist com memória persistente."""
    
    # Obter contexto das memórias anteriores
    memory_context = memory_manager.get_context_summary()
    
    agent = Agent(
        name="Assistente Todoist com Memória",
        instructions=f"""Você é um assistente especializado em gerenciar tarefas no Todoist com memória persistente.
        
        Você pode:
        - Listar, adicionar e completar tarefas no Todoist
        - Lembrar preferências e informações do usuário
        - Recuperar informações armazenadas anteriormente
        - Mostrar todas as memórias armazenadas
        - Limpar memórias quando solicitado
        
        {memory_context}
        
        Use a memória para personalizar suas respostas e lembrar de preferências do usuário.
        Seja proativo em sugerir ações baseadas no que você sabe sobre o usuário.""",
        tools=[
            # Ferramentas do Todoist
            list_todoist_tasks,
            add_todoist_task,
            complete_todoist_task,
            list_completed_tasks,
            # Ferramentas de memória
            remember_preference,
            recall_preference,
            show_all_memories,
            clear_all_memories
        ],
        model=OpenRouter(
            id=DEFAULT_MODEL,
            api_key=OPENROUTER_API_KEY
        ),
        add_history_to_context=True,
        num_history_runs=10,
        markdown=True,
        storage=SqliteStorage(
            db_file="storage/todoist_memory_assistant.db",
            table_name="interactions"
        )
    )
    
    return agent


def main():
    """Função principal para executar o assistente com memória."""
    # Criar o agente
    agent = create_todoist_assistant_with_memory()
    
    # Criar o AgentOS
    agent_os = AgentOS(
        os_id="todoist-assistant-memory-v1",
        description="Assistente Todoist com memória persistente avançada",
        agents=[agent],
        interfaces=[AGUI(agent=agent)],
        telemetry=True,
        enable_mcp=True,
        storage=SqliteStorage(
            db_file="storage/agentos_memory.db",
            table_name="agentos_data"
        )
    )
    
    # Obter a aplicação FastAPI
    app = agent_os.get_app()
    
    print("╔══════════════════════════════════════════════════════╗")
    print("║   🧠 Assistente Todoist com Memória Persistente     ║")
    print("╚══════════════════════════════════════════════════════╝")
    print()
    print("📍 Endpoints disponíveis:")
    print(f"  • http://localhost:{AGENTOS_DEFAULT_PORT}/docs    - Documentação da API")
    print(f"  • http://localhost:{AGENTOS_DEFAULT_PORT}/config  - Configuração do AgentOS")
    print(f"  • http://localhost:{AGENTOS_DEFAULT_PORT}/memory  - Visualizar memórias")
    print(f"  • http://localhost:{AGENTOS_DEFAULT_PORT}/history - Histórico de interações")
    print(f"  • http://localhost:{AGENTOS_DEFAULT_PORT}/mcp     - MCP Server endpoint")
    print()
    print("🧠 Recursos de Memória:")
    print("  • Lembra preferências do usuário")
    print("  • Mantém contexto entre conversas")
    print("  • Personaliza respostas baseadas no histórico")
    print("  • Armazenamento persistente de informações")
    print()
    print("💡 Exemplos de comandos:")
    print("  • Lembre que meu projeto prioritário é o App Mobile")
    print("  • Qual é meu projeto prioritário?")
    print("  • Mostre tudo que você lembra sobre mim")
    print("  • Liste minhas tarefas do projeto prioritário")
    print("  • Limpe todas as memórias")
    print()
    print("🚀 Iniciando servidor com memória...")
    print()
    
    agent_os.serve(
        app="src.assistants.todoist_with_memory:app",
        port=AGENTOS_DEFAULT_PORT
    )


# Criar app para importação
agent = create_todoist_assistant_with_memory()
agent_os = AgentOS(
    os_id="todoist-assistant-memory-v1",
    description="Assistente Todoist com memória persistente avançada",
    agents=[agent],
    interfaces=[AGUI(agent=agent)],
    telemetry=True,
    enable_mcp=True,
    storage=SqliteStorage(
        db_file="storage/agentos_memory.db",
        table_name="agentos_data"
    )
)
app = agent_os.get_app()


if __name__ == "__main__":
    main()
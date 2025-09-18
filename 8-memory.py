import os
from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from agno.models.openrouter import OpenRouter
from agno.memory.manager import MemoryManager
from agno.os import AgentOS
from agno.os.interfaces.agui import AGUI
from agno.db.sqlite import SqliteDb
from dotenv import load_dotenv

load_dotenv()

# Configurar banco SQLite para memória persistente
db = SqliteDb(
    db_file="data/todoist_memory.db",
    session_table="agent_sessions"
)

# Configurar o MemoryManager
memory_manager = MemoryManager(
    memory_capture_instructions="""
        Colete as seguintes informações sobre o usuário:
        - Nome completo
        - Preferências de organização de tarefas
        - Horários preferidos para trabalhar
        - Tipos de projetos que trabalha
        - Metas e objetivos pessoais
        - Ferramentas de produtividade que usa além do Todoist
    """,
    model=OpenRouter(
        id="openai/gpt-4o-mini",
        api_key=os.getenv("OPENROUTER_API_KEY")
    ),
)

agent = Agent(
    name="Assistente Todoist",
    instructions="""Você é um pesquisador especialista em produtividade e organização de tarefas usando Todoist.
    Seu objetivo é ajudar os usuários a gerenciar suas tarefas de forma eficiente.
    
    IMPORTANTE: 
    - Você tem memória persistente ativada. Lembre-se de informações importantes sobre o usuário.
    - Use as memórias armazenadas para personalizar suas respostas.
    - Sempre que possível, utilize os recursos do Todoist para listar, adicionar e completar tarefas.
    - Seja claro e objetivo em suas respostas.""",
    tools=[TavilyTools()],
    model=OpenRouter(
        id="openai/gpt-4o-mini",
        api_key=os.getenv("OPENROUTER_API_KEY")
    ),
    db=db,
    memory_manager=memory_manager,
    enable_user_memories=True,
    add_history_to_context=True,
    num_history_runs=3,
    markdown=True,
    debug_mode=True,  # Ativa debug para ver o que está acontecendo
)

# Criar o AgentOS com configurações avançadas
agent_os = AgentOS(
    os_id="todoist-memory-v2",  # ID único atualizado
    description="Assistente Todoist com memória persistente",
    agents=[agent],
    interfaces=[AGUI(agent=agent)],  # Interface AGUI
    telemetry=True,  # Ativa telemetria para analytics
    enable_mcp=True,  # Ativa MCP server para integração externa
)

# Obter a aplicação FastAPI
app = agent_os.get_app()

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🧠 ASSISTENTE TODOIST COM MEMÓRIA PERSISTENTE")
    print("="*60)
    print("\n📍 Acesse: http://localhost:7790")
    print("\n💡 TESTE A MEMÓRIA:")
    print("1. Diga: 'Meu nome é [seu nome] e trabalho com [área]'")
    print("2. Pergunte: 'O que você lembra sobre mim?'")
    print("3. A aba Memory no painel deve mostrar as informações")
    print("\n⚠️  Nota: O user_id é gerado automaticamente pelo AGUI")
    print("="*60 + "\n")
    
    # Serve sem reload quando usando MCP
    agent_os.serve(app="8-memory:app", port=7790)

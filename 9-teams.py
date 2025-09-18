import os
from agno.agent import Agent
from agno.team import Team
from agno.tools.tavily import TavilyTools
from agno.models.openrouter import OpenRouter
from agno.os import AgentOS
from agno.os.interfaces.agui import AGUI
from dotenv import load_dotenv

load_dotenv()

# Configurar modelo compartilhado
model = OpenRouter(
    id="openai/gpt-4o-mini",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# Agente Pesquisador
researcher = Agent(
    name="Pesquisador",
    role="Especialista em Pesquisa",
    instructions="""Você é um pesquisador especializado em buscar informações detalhadas.
    Sua função é:
    - Pesquisar informações relevantes sobre o tópico solicitado
    - Fornecer dados atualizados e precisos
    - Citar fontes quando possível""",
    tools=[TavilyTools()],
    model=model,
    markdown=True
)

# Agente Analista
analyst = Agent(
    name="Analista",
    role="Analista de Dados",
    instructions="""Você é um analista especializado em interpretar dados e informações.
    Sua função é:
    - Analisar as informações fornecidas pelo pesquisador
    - Identificar padrões e insights
    - Criar resumos estruturados""",
    model=model,
    markdown=True
)

# Agente Redator
writer = Agent(
    name="Redator",
    role="Especialista em Conteúdo",
    instructions="""Você é um redator especializado em criar conteúdo claro e engajante.
    Sua função é:
    - Transformar análises em conteúdo legível
    - Estruturar informações de forma clara
    - Criar conclusões e recomendações""",
    model=model,
    markdown=True
)

# Criar o Time de Agentes
team = Team(
    name="Time de Análise",
    role="Time especializado em análise e produção de conteúdo",
    members=[researcher, analyst, writer],  # Parâmetro correto é 'members'
    model=model,
    instructions="""Vocês são um time especializado em análise e produção de conteúdo.
    
    FLUXO DE TRABALHO:
    1. O Pesquisador busca informações sobre o tópico
    2. O Analista interpreta os dados encontrados
    3. O Redator cria um relatório final estruturado
    
    Trabalhem em sequência para entregar o melhor resultado possível.""",
    markdown=True,
    debug_mode=True
)

# Criar o AgentOS com o Team
agent_os = AgentOS(
    os_id="team-analysis-v1",
    description="Sistema de análise com time de agentes especializados",
    teams=[team],  # Usa teams em vez de agents
    interfaces=[AGUI(team=team)],  # Interface AGUI com team
    telemetry=True,
    enable_mcp=True
)

# Obter a aplicação FastAPI
app = agent_os.get_app()

if __name__ == "__main__":
    print("\n" + "="*60)
    print("👥 SISTEMA DE ANÁLISE COM TIME DE AGENTES")
    print("="*60)
    print("\n📍 Acesse: http://localhost:7791")
    print("\n🤝 TIME DISPONÍVEL:")
    print("   • Pesquisador - Busca informações")
    print("   • Analista - Interpreta dados")
    print("   • Redator - Cria conteúdo final")
    print("\n💡 EXEMPLOS DE USO:")
    print("1. 'Analise as tendências de IA em 2024'")
    print("2. 'Pesquise sobre energia renovável no Brasil'")
    print("3. 'Crie um relatório sobre produtividade remota'")
    print("="*60 + "\n")
    
    # Serve na porta 7791 para não conflitar
    agent_os.serve(app="9-teams:app", port=7791)
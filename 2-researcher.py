from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from agno.models.openrouter import OpenRouter
import os

from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    tools=[TavilyTools()],
    debug_mode=True,  # Mencionar após na apresentação
    model=OpenRouter(
        id="openai/gpt-4o-mini",
        api_key=os.getenv("OPENROUTER_API_KEY")
    )
)

agent.print_response(
    'Como estão o desempenho das ações da Apple e da Microsoft nos últimos 6 meses? E qual é a previsão para os próximos 3 meses?'
)

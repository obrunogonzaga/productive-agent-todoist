from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from agno.tools.yfinance import YFinanceTools
from agno.models.openrouter import OpenRouter
import os

from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    tools=[TavilyTools(), YFinanceTools()],
    debug_mode=True,
    instructions="Use tabelas para mostrar a informação final. Não inclua nenhum outro texto",
    model=OpenRouter(
        id="openai/gpt-4o-mini",
        api_key=os.getenv("OPENROUTER_API_KEY")
    )
)

agent.print_response(
    'Qual a cotação atual da APPLE?'
)

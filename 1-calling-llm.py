from agno.models.openrouter import OpenRouter
from agno.models.message import Message
from dotenv import load_dotenv
import os

load_dotenv()


model = OpenRouter(
    id="openai/gpt-4o-mini",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

msg = Message(
    role="user",
    content=[{"type": "text", "text": "Olá, Mundo!"}],
)

assistant_message = Message(role="assistant", content=[])

response = model.invoke([msg], assistant_message)
print(response.content)

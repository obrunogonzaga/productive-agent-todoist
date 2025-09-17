from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.tools import tool
import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Optional

load_dotenv()

# Configuração da API do Todoist
TODOIST_API_KEY = os.getenv("TODOIST_API_KEY")
TODOIST_BASE_URL = "https://api.todoist.com/rest/v2"
TODOIST_HEADERS = {
    "Authorization": f"Bearer {TODOIST_API_KEY}",
    "Content-Type": "application/json"
}


@tool
def list_todoist_tasks(filter: Optional[str] = None) -> str:
    """
    Lista tarefas do Todoist com filtros opcionais.
    
    Args:
        filter: Filtro opcional para as tarefas. Pode ser:
               - "hoje" ou "today": tarefas de hoje
               - "amanhã" ou "tomorrow": tarefas de amanhã  
               - "semana" ou "week": tarefas desta semana
               - "vencidas" ou "overdue": tarefas vencidas
               - None: todas as tarefas
    """
    # Construir parâmetros de filtro baseado na entrada
    params = {}
    
    if filter:
        filter_lower = filter.lower()
        today = datetime.now().date()
        
        if filter_lower in ["hoje", "today"]:
            # Tarefas com data de hoje
            params["filter"] = f"due today"
        elif filter_lower in ["amanhã", "amanha", "tomorrow"]:
            # Tarefas com data de amanhã
            params["filter"] = f"due tomorrow"
        elif filter_lower in ["semana", "week", "esta semana", "this week"]:
            # Tarefas para os próximos 7 dias
            end_date = today + timedelta(days=7)
            params["filter"] = f"due before: {end_date.strftime('%Y-%m-%d')}"
        elif filter_lower in ["vencidas", "overdue", "atrasadas"]:
            # Tarefas vencidas
            params["filter"] = "overdue"
        elif "próximos" in filter_lower or "next" in filter_lower:
            # Extrair número de dias se especificado
            import re
            days_match = re.search(r'(\d+)', filter_lower)
            if days_match:
                days = int(days_match.group(1))
                end_date = today + timedelta(days=days)
                params["filter"] = f"due before: {end_date.strftime('%Y-%m-%d')}"
    
    response = requests.get(
        f"{TODOIST_BASE_URL}/tasks",
        headers=TODOIST_HEADERS,
        params=params
    )
    
    if response.status_code == 200:
        tasks = response.json()
        if not tasks:
            filter_msg = f" com filtro '{filter}'" if filter else ""
            return f"Nenhuma tarefa encontrada no Todoist{filter_msg}"
        
        filter_msg = f" ({filter})" if filter else ""
        result = f"📋 Suas tarefas no Todoist{filter_msg}:\n"
        
        for task in tasks[:20]:  # Aumentando para 20 tarefas
            # Adicionar indicador de data se houver
            due_info = ""
            if task.get('due'):
                due_date = task['due'].get('date', '')
                due_time = task['due'].get('datetime', '')
                
                if due_date:
                    try:
                        # Verificar se tem horário específico
                        if due_time:
                            task_datetime = datetime.strptime(due_time, '%Y-%m-%dT%H:%M:%S')
                            task_date = task_datetime.date()
                            time_str = task_datetime.strftime('%H:%M')
                        else:
                            task_date = datetime.strptime(due_date, '%Y-%m-%d').date()
                            time_str = None
                        
                        # Formatação baseada na data
                        if task_date == today:
                            time_part = f" às {time_str}" if time_str else ""
                            due_info = f" 📅 [HOJE{time_part}]"
                        elif task_date == today + timedelta(days=1):
                            time_part = f" às {time_str}" if time_str else ""
                            due_info = f" 📅 [AMANHÃ{time_part}]"
                        elif task_date < today:
                            days_overdue = (today - task_date).days
                            due_info = f" ⚠️ [VENCIDA há {days_overdue} dia{'s' if days_overdue != 1 else ''}]"
                        else:
                            # Formatar data em português
                            formatted_date = task_date.strftime('%d/%m')
                            time_part = f" às {time_str}" if time_str else ""
                            due_info = f" 📅 [{formatted_date}{time_part}]"
                    except:
                        due_info = f" 📅 [{due_date}]"
            
            # Adicionar prioridade
            priority_emoji = ""
            if task.get('priority', 1) == 4:
                priority_emoji = "🔴 "
            elif task.get('priority', 1) == 3:
                priority_emoji = "🟡 "
            elif task.get('priority', 1) == 2:
                priority_emoji = "🔵 "
            
            # Status da tarefa (todas são ativas/não concluídas nesta função)
            status_emoji = "⬜"  # Checkbox vazio para tarefas não concluídas
            
            result += f"{status_emoji} {priority_emoji}[{task['id']}] {task['content']}{due_info}\n"
        
        return result
    else:
        return f"Erro ao listar tarefas: {response.status_code}"


@tool
def add_todoist_task(content: str, due_date: Optional[str] = None, priority: int = 1) -> str:
    """
    Adiciona uma nova tarefa ao Todoist com data opcional.
    
    Args:
        content: Descrição da tarefa a ser adicionada
        due_date: Data de vencimento opcional. Pode ser:
                 - "hoje" ou "today": para hoje
                 - "amanhã" ou "tomorrow": para amanhã
                 - Uma data no formato "YYYY-MM-DD"
                 - "próxima segunda", "next monday", etc.
        priority: Prioridade da tarefa (1-4, onde 4 é urgente)
    """
    data = {
        "content": content,
        "priority": priority
    }
    
    # Processar data de vencimento se fornecida
    if due_date:
        due_date_lower = due_date.lower()
        today = datetime.now().date()
        
        if due_date_lower in ["hoje", "today"]:
            data["due_date"] = today.strftime("%Y-%m-%d")
        elif due_date_lower in ["amanhã", "amanha", "tomorrow"]:
            tomorrow = today + timedelta(days=1)
            data["due_date"] = tomorrow.strftime("%Y-%m-%d")
        elif "próxima" in due_date_lower or "next" in due_date_lower:
            # Mapear dias da semana
            weekdays = {
                "segunda": 0, "monday": 0,
                "terça": 1, "tuesday": 1,
                "quarta": 2, "wednesday": 2,
                "quinta": 3, "thursday": 3,
                "sexta": 4, "friday": 4,
                "sábado": 5, "saturday": 5,
                "domingo": 6, "sunday": 6
            }
            
            for day_name, day_num in weekdays.items():
                if day_name in due_date_lower:
                    days_ahead = day_num - today.weekday()
                    if days_ahead <= 0:  # Já passou nesta semana
                        days_ahead += 7
                    target_date = today + timedelta(days=days_ahead)
                    data["due_date"] = target_date.strftime("%Y-%m-%d")
                    break
        else:
            # Assumir formato YYYY-MM-DD ou tentar interpretar
            try:
                # Tentar parse direto
                parsed_date = datetime.strptime(due_date, "%Y-%m-%d")
                data["due_date"] = due_date
            except ValueError:
                # Tentar outros formatos comuns
                for fmt in ["%d/%m/%Y", "%d-%m-%Y", "%d/%m", "%d-%m"]:
                    try:
                        parsed_date = datetime.strptime(due_date, fmt)
                        # Se o ano não foi especificado, usar o ano atual
                        if fmt in ["%d/%m", "%d-%m"]:
                            parsed_date = parsed_date.replace(year=today.year)
                        data["due_date"] = parsed_date.strftime("%Y-%m-%d")
                        break
                    except ValueError:
                        continue
    
    response = requests.post(
        f"{TODOIST_BASE_URL}/tasks",
        headers=TODOIST_HEADERS,
        json=data
    )
    
    if response.status_code == 200:
        task = response.json()
        due_info = ""
        if task.get("due") and task["due"].get("date"):
            due_info = f" 📅 para {task['due']['date']}"
        return f"✅ Tarefa adicionada: {task['content']}{due_info} (ID: {task['id']})"
    else:
        return f"Erro ao adicionar tarefa: {response.status_code}"


@tool
def complete_todoist_task(task_id: str) -> str:
    """
    Marca uma tarefa como concluída no Todoist.
    
    Args:
        task_id: ID da tarefa a ser completada
    """
    response = requests.post(
        f"{TODOIST_BASE_URL}/tasks/{task_id}/close",
        headers=TODOIST_HEADERS
    )
    
    if response.status_code == 204:
        return f"✅ Tarefa {task_id} marcada como concluída!"
    else:
        return f"Erro ao completar tarefa: {response.status_code}"


@tool
def list_completed_tasks(limit: int = 20) -> str:
    """
    Lista tarefas concluídas recentemente no Todoist.
    
    Args:
        limit: Número máximo de tarefas concluídas a retornar (padrão: 20)
    """
    # A API v2 do Todoist usa um endpoint diferente para tarefas concluídas
    sync_url = "https://api.todoist.com/sync/v9/completed/get_all"
    
    params = {
        "limit": limit
    }
    
    response = requests.get(
        sync_url,
        headers=TODOIST_HEADERS,
        params=params
    )
    
    if response.status_code == 200:
        data = response.json()
        completed_items = data.get('items', [])
        
        if not completed_items:
            return "Nenhuma tarefa concluída encontrada"
        
        result = "✅ Tarefas concluídas recentemente:\n"
        
        for task in completed_items:
            # Formatar data de conclusão
            completed_date_str = task.get('completed_at', '')
            completed_info = ""
            
            if completed_date_str:
                try:
                    completed_datetime = datetime.strptime(completed_date_str, '%Y-%m-%dT%H:%M:%S')
                    completed_date = completed_datetime.date()
                    today = datetime.now().date()
                    
                    if completed_date == today:
                        completed_info = f" [Concluída HOJE às {completed_datetime.strftime('%H:%M')}]"
                    elif completed_date == today - timedelta(days=1):
                        completed_info = f" [Concluída ONTEM às {completed_datetime.strftime('%H:%M')}]"
                    else:
                        completed_info = f" [Concluída em {completed_date.strftime('%d/%m às %H:%M')}]"
                except:
                    completed_info = f" [Concluída em {completed_date_str}]"
            
            # Status da tarefa concluída
            status_emoji = "✅"  # Checkbox marcado para tarefas concluídas
            
            result += f"{status_emoji} {task.get('content', 'Sem título')}{completed_info}\n"
        
        return result
    else:
        return f"Erro ao listar tarefas concluídas: {response.status_code}"


# Criar o agente com as ferramentas do Todoist
agent = Agent(
    tools=[list_todoist_tasks, add_todoist_task, complete_todoist_task, list_completed_tasks],
    model=OpenRouter(
        id="openai/gpt-4o-mini",
        api_key=os.getenv("OPENROUTER_API_KEY")
    )
)

# Chat interativo
print("🤖 Assistente Todoist iniciado!")
print("💡 Exemplos de comandos:")
print("   - 'Liste minhas tarefas'")
print("   - 'Liste as tarefas de hoje'")
print("   - 'Mostre as tarefas de amanhã'")
print("   - 'Quais são as tarefas desta semana?'")
print("   - 'Liste tarefas vencidas'")
print("   - 'Mostre tarefas concluídas'")
print("   - 'Adicione uma tarefa: Estudar Python'")
print("   - 'Adicione tarefa: Reunião amanhã'")
print("   - 'Crie tarefa: Entrega do projeto para próxima sexta'")
print("   - 'Complete a tarefa 8554911084'")
print("   - 'sair' para encerrar\n")

while True:
    user_input = input("Você: ")
    
    if user_input.lower() in ['sair', 'exit', 'quit']:
        print("👋 Até logo!")
        break
    
    agent.print_response(user_input)
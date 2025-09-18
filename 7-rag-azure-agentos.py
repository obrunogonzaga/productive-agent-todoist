#!/usr/bin/env python
"""
Azure AZ-104 Assistant com RAG usando AgentOS
Sistema completo com interface web para consultas sobre Azure
"""

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.os import AgentOS
from agno.os.interfaces.agui import AGUI
from agno.db.sqlite import SqliteDb
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.knowledge.embedder.openai import OpenAIEmbedder
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

print("\n╔══════════════════════════════════════════════════════╗")
print("║     ☁️  Azure AZ-104 Assistant com AgentOS            ║")
print("╚══════════════════════════════════════════════════════╝")

# Configurar banco de dados para persistência de sessões
print("\n🗄️  Configurando banco de dados...")
db = SqliteDb(db_file="data/azure_assistant.db")

# Configurar Knowledge Base com LanceDB para embeddings
print("📚 Configurando Knowledge Base...")
knowledge = Knowledge(
    name="Azure AZ-104 Knowledge Base",
    description="Base de conhecimento com o guia completo Azure AZ-104",
    vector_db=LanceDb(
        table_name="azure_az104_docs",
        uri="data/azure_lancedb",
        search_type=SearchType.vector,
        embedder=OpenAIEmbedder(
            id="text-embedding-3-small",
            api_key=os.getenv("OPENAI_API_KEY")
        ),
    ),
)

# Verificar se precisa carregar o PDF
lancedb_path = Path("data/azure_lancedb/azure_az104_docs.lance")
if not lancedb_path.exists():
    print("\n📄 Primeira execução - Carregando PDF Azure AZ-104...")
    print("⏳ Isso pode levar alguns minutos na primeira vez...")
    try:
        knowledge.add_content(
            name="Azure AZ-104 Administrator Guide",
            path="az-104-Microsoft-Azure-Administrator.pdf",
            metadata={
                "tipo": "certificação",
                "área": "cloud computing",
                "provider": "Microsoft Azure"
            }
        )
        print("✅ PDF Azure AZ-104 carregado com sucesso!")
    except Exception as e:
        print(f"⚠️  Aviso ao carregar PDF: {e}")
        print("   Continuando com base existente...")
else:
    print("✅ Base de conhecimento Azure já carregada!")
    # Testar busca para confirmar funcionamento
    print("\n🔍 Testando busca na knowledge base...")
    try:
        test_results = knowledge.search("virtual network")
        if test_results:
            print(f"✅ Knowledge base funcionando! {len(test_results)} resultados encontrados")
        else:
            print("⚠️  Nenhum resultado encontrado no teste")
    except Exception as e:
        print(f"❌ Erro ao testar knowledge base: {e}")

# Criar o agente especialista em Azure
print("\n🤖 Configurando Azure AZ-104 Expert Agent...")
agent = Agent(
    name="Azure AZ-104 Expert",
    instructions="""Você é um especialista certificado em Microsoft Azure AZ-104.
    
    USE SEMPRE a base de conhecimento RAG do PDF AZ-104 para responder.
    Seja técnico e preciso, citando conceitos específicos do guia quando possível.
    
    Áreas de especialização:
    • Azure Virtual Networks e Networking (VNet, Subnets, NSGs, Peering)
    • Storage Accounts (Blob, File, Queue, Table, replicação)
    • Azure AD / Entra ID (Users, Groups, RBAC, MFA)
    • Compute Services (VMs, Scale Sets, App Services, Container Instances)
    • Monitoring e Backup (Azure Monitor, Log Analytics, Backup, Recovery)
    • Security e Compliance (Key Vault, Policies, Security Center)
    • Resource Management (ARM templates, Tags, Locks, Cost Management)
    
    IMPORTANTE ao responder:
    1. Sempre busque informações na base de conhecimento primeiro
    2. Cite seções ou conceitos específicos do guia AZ-104
    3. Forneça exemplos práticos quando apropriado
    4. Use a terminologia correta do Azure
    5. Indique comandos Azure CLI ou PowerShell quando relevante
    
    Formato de resposta:
    - Seja claro e estruturado
    - Use bullet points para listas
    - Destaque comandos e configurações importantes
    - Sempre que possível, mencione best practices do Azure""",
    model=OpenRouter(
        id="openai/gpt-4o-mini",
        api_key=os.getenv("OPENROUTER_API_KEY")
    ),
    knowledge=knowledge,
    db=db,
    session_id="azure_session",
    add_history_to_context=True,
    num_history_runs=5,
    search_knowledge=True,  # Busca automática na knowledge base
    add_knowledge_to_context=True,  # Adiciona contexto relevante ao prompt
    markdown=True,
    debug_mode=False  # Desativar debug em produção
)

# Criar o AgentOS com interface web
print("🌐 Configurando AgentOS com interface web...")
agent_os = AgentOS(
    os_id="azure-az104-assistant-v1",
    description="Azure AZ-104 Assistant com RAG e Interface Web",
    agents=[agent],
    interfaces=[
        AGUI(agent=agent)
    ],
    telemetry=True,
    enable_mcp=True
)

# Obter a aplicação FastAPI
app = agent_os.get_app()

# Função de teste do RAG
def test_azure_rag():
    """Teste manual do sistema RAG com Azure"""
    print("\n" + "="*60)
    print("🧪 TESTE DO SISTEMA RAG - AZURE AZ-104")
    print("="*60)
    
    test_queries = [
        "What are the different types of storage replication in Azure?",
        "How to configure Network Security Groups?",
        "Explain Azure RBAC roles"
    ]
    
    for query in test_queries:
        print(f"\n📝 Testando: {query}")
        print("-"*40)
        
        try:
            # Buscar na knowledge base
            results = knowledge.search(query)
            
            if results:
                print(f"✅ {len(results)} resultados encontrados")
                print(f"   Top resultado (score: {results[0].get('score', 0):.4f})")
                print(f"   Trecho: {results[0].get('content', '')[:150]}...")
            else:
                print("❌ Nenhum resultado encontrado")
                
        except Exception as e:
            print(f"❌ Erro no teste: {e}")
    
    print("\n" + "="*60)

# Iniciar o servidor
if __name__ == "__main__":
    print("\n╔══════════════════════════════════════════════════════╗")
    print("║     🚀 Azure AZ-104 Assistant - AgentOS Ready!        ║")
    print("╚══════════════════════════════════════════════════════╝")
    print()
    print("📚 Knowledge Base: Azure AZ-104 Administrator Guide PDF")
    print("🔧 Model: GPT-4o-mini via OpenRouter")
    print("💾 Database: SQLite com persistência de sessões")
    print()
    
    # Oferecer teste opcional
    if input("🧪 Deseja executar teste do RAG? (s/n): ").lower() == 's':
        test_azure_rag()
    
    print("\n📍 Endpoints disponíveis:")
    print("  • http://localhost:7780         - Interface Web AGUI")
    print("  • http://localhost:7780/docs    - Documentação da API")
    print("  • http://localhost:7780/config  - Configuração do AgentOS")
    print("  • http://localhost:7780/agents  - Listar agentes")
    print()
    print("💡 Perguntas sugeridas para testar:")
    print("  • What are the Azure storage account tiers?")
    print("  • How to configure VNet peering?")
    print("  • Explain Azure Backup policies")
    print("  • What are Network Security Group rules?")
    print("  • How to implement Azure RBAC?")
    print()
    print("🌐 Iniciando servidor na porta 7780...")
    print("   Acesse http://localhost:7780 para usar a interface web")
    print()

    agent_os.serve(app="7-rag-azure-agentos:app", port=7780)
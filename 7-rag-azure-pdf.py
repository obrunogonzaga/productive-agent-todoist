#!/usr/bin/env python
"""
RAG Simples com PDF Azure AZ-104
Demonstração mínima de RAG para apresentação
"""

from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.models.openrouter import OpenRouter
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.knowledge.embedder.openai import OpenAIEmbedder
import os
from dotenv import load_dotenv

load_dotenv()

print("\n╔══════════════════════════════════════════════════════╗")
print("║     ☁️  Azure AZ-104 Assistant com RAG               ║")
print("╚══════════════════════════════════════════════════════╝")

# Configurar Knowledge Base simples
print("\n📚 Configurando Knowledge Base...")
knowledge = Knowledge(
    vector_db=LanceDb(
        table_name="azure_az104",
        uri="tmp/azure_rag",
        search_type=SearchType.vector,
        embedder=OpenAIEmbedder(
            id="text-embedding-3-small",
            api_key=os.getenv("OPENAI_API_KEY")
        ),
    ),
)

# Carregar PDF do Azure
print("📄 Carregando PDF Azure AZ-104...")
print("   (Isso pode levar alguns minutos na primeira vez...)")
try:
    knowledge.add_content(
        name="Azure AZ-104 Guide",
        path="az-104-Microsoft-Azure-Administrator.pdf"
    )
    print("✅ PDF carregado com sucesso!")
except Exception as e:
    print(f"⚠️  Aviso: {e}")
    print("   Continuando com base existente...")

# Criar agente Azure
print("\n🤖 Configurando Azure Expert Agent...")
agent = Agent(
    name="Azure AZ-104 Expert",
    model=OpenRouter(
        id="openai/gpt-4o-mini",
        api_key=os.getenv("OPENROUTER_API_KEY")
    ),
    knowledge=knowledge,
    add_knowledge_to_context=True,
    search_knowledge=True,
    markdown=True,
    instructions="""Você é um especialista certificado em Microsoft Azure AZ-104.
    
    Use SEMPRE a base de conhecimento RAG do PDF AZ-104 para responder.
    Seja técnico e preciso, citando conceitos do guia quando possível.
    
    Especialidades:
    - Azure Virtual Networks e Networking
    - Storage Accounts e serviços
    - Azure AD / Entra ID
    - Compute (VMs, App Services)
    - Monitoring e Backup
    - Security e Compliance"""
)

print("✅ Sistema pronto!")
print("\n" + "="*60)
print("💬 Chat com RAG - Azure AZ-104")
print("="*60)
print("\n📝 Pergunte sobre:")
print("  • Virtual Networks e Subnets")
print("  • Storage Accounts e replicação")
print("  • Azure Active Directory")
print("  • Network Security Groups")
print("  • Virtual Machines")
print("\nDigite 'sair' para encerrar")
print("-"*60)

# Loop de chat
while True:
    query = input("\n🧑 Você: ").strip()
    
    if query.lower() in ['sair', 'exit', 'quit']:
        break
    
    if not query:
        continue
    
    print("\n🤖 Azure Expert:")
    print("-"*40)
    
    # Debug RAG (opcional - remover para produção)
    print("🔍 [RAG] Buscando no PDF AZ-104...")
    results = knowledge.search(query)
    if results:
        print(f"   ✓ {len(results)} trechos relevantes encontrados")
    print()
    
    # Resposta
    agent.print_response(query, stream=True)
    print("\n" + "-"*40)

print("\n✨ Obrigado por testar o RAG com Azure AZ-104!")
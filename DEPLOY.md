# 🚀 Deploy do Assistente Todoist no Coolify

Este guia mostra como fazer deploy do Assistente Todoist AgentOS no Coolify.

## 📋 Pré-requisitos

- Coolify instalado e configurado na sua VPS
- Acesso SSH à VPS
- API Keys necessárias:
  - Todoist API Key
  - OpenRouter API Key

## 🔧 Configuração no Coolify

### Opção 1: Deploy via GitHub (Recomendado)

1. **No Coolify, crie um novo recurso:**
   - Clique em "New Resource"
   - Selecione "Docker Compose"
   - Escolha "Public Repository"

2. **Configure o repositório:**
   ```
   Repository URL: https://github.com/obrunogonzaga/productive-agent-todoist
   Branch: main
   Docker Compose Location: /docker-compose.production.yml
   ```

3. **Configure as variáveis de ambiente:**
   - Vá em "Environment Variables"
   - Adicione as seguintes variáveis:
   ```env
   TODOIST_API_KEY=sua_api_key_todoist
   OPENROUTER_API_KEY=sua_api_key_openrouter
   DOMAIN=todoist.seudominio.com
   PORT=7777
   
   # Opcional - para segurança
   OS_SECURITY_KEY=gere_uma_chave_forte_aqui
   ```

4. **Configure o domínio:**
   - Em "Domains", adicione seu domínio
   - Configure o proxy reverso para porta 7777

5. **Deploy:**
   - Clique em "Deploy"
   - Aguarde o build e início do container

### Opção 2: Deploy Manual via SSH

1. **Clone o repositório na VPS:**
   ```bash
   git clone https://github.com/obrunogonzaga/productive-agent-todoist.git
   cd productive-agent-todoist
   ```

2. **Crie o arquivo .env:**
   ```bash
   cp .env.example .env
   nano .env
   ```
   
   Configure as variáveis:
   ```env
   TODOIST_API_KEY=sua_api_key_todoist
   OPENROUTER_API_KEY=sua_api_key_openrouter
   DOMAIN=todoist.seudominio.com
   ```

3. **Execute com Docker Compose:**
   ```bash
   docker-compose -f docker-compose.production.yml up -d
   ```

4. **Configure no Coolify:**
   - Adicione como "Existing Docker Container"
   - Configure o proxy reverso

## 🔒 Segurança

### Proteger os endpoints com Security Key:

1. **Gere uma chave forte:**
   ```bash
   openssl rand -hex 32
   ```

2. **Configure a variável de ambiente:**
   ```env
   OS_SECURITY_KEY=sua_chave_gerada
   ```

3. **Use nas requisições:**
   ```bash
   curl -H "Authorization: Bearer sua_chave_gerada" \
        https://todoist.seudominio.com/config
   ```

## 📊 Endpoints Disponíveis

Após o deploy, você terá acesso aos seguintes endpoints:

- `https://todoist.seudominio.com/docs` - Documentação da API
- `https://todoist.seudominio.com/config` - Configuração do AgentOS
- `https://todoist.seudominio.com/agents` - Listar agentes
- `https://todoist.seudominio.com/runs` - Histórico de execuções
- `https://todoist.seudominio.com/mcp` - MCP Server endpoint

## 🧪 Testando o Deploy

1. **Verificar health:**
   ```bash
   curl https://todoist.seudominio.com/config
   ```

2. **Testar o agente:**
   ```bash
   curl -X POST https://todoist.seudominio.com/agent/run \
        -H "Content-Type: application/json" \
        -d '{"agent_id": "assistente-todoist", "input": "Liste minhas tarefas"}'
   ```

## 🔄 Atualizações

Para atualizar a aplicação:

1. **Via Coolify:**
   - Clique em "Redeploy"
   - O Coolify pegará as últimas mudanças do GitHub

2. **Manual:**
   ```bash
   git pull
   docker-compose -f docker-compose.production.yml down
   docker-compose -f docker-compose.production.yml up -d --build
   ```

## 🐛 Troubleshooting

### Logs do container:
```bash
docker logs todoist-agent
```

### Verificar status:
```bash
docker ps | grep todoist-agent
```

### Reiniciar o serviço:
```bash
docker-compose -f docker-compose.production.yml restart
```

## 🔗 Integrações

### Conectar com a UI existente:

Se você já tem a Agent UI rodando no Coolify, configure ela para apontar para este backend:

1. Na configuração da Agent UI, defina:
   ```env
   NEXT_PUBLIC_DEFAULT_ENDPOINT=https://todoist.seudominio.com
   ```

2. Se usar Security Key, configure também na UI.

## 📝 Notas

- O AgentOS expõe automaticamente uma API REST completa
- Todos os endpoints são documentados em `/docs`
- O MCP server em `/mcp` permite integrações externas
- Para persistência de dados, descomente a seção PostgreSQL no docker-compose

## 🆘 Suporte

Para problemas ou dúvidas:
- Abra uma issue no [GitHub](https://github.com/obrunogonzaga/productive-agent-todoist/issues)
- Verifique os logs do container
- Consulte a documentação do [Agno](https://docs.agno.com)
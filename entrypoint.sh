#!/bin/bash
set -e

echo "🚀 Starting Todoist AgentOS..."
echo "Environment variables are set by Coolify"

# Simply execute the Python application
# The Python code already uses os.getenv() which reads from environment
# No need to create .env file - it will work with environment variables directly
exec python 5-assistente-agentOS.py
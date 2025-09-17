#!/bin/bash
set -e

# Create .env file from environment variables if it doesn't exist
if [ ! -f /app/.env ]; then
    echo "Creating .env file from environment variables..."
    
    # Write environment variables to .env file
    cat > /app/.env << EOF
TODOIST_API_KEY=${TODOIST_API_KEY}
OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
OS_SECURITY_KEY=${OS_SECURITY_KEY:-}
AGNO_API_KEY=${AGNO_API_KEY:-}
AGNO_MONITOR=${AGNO_MONITOR:-false}
EOF
    
    echo ".env file created successfully"
else
    echo "Using existing .env file"
fi

# Execute the main application
exec python 5-assistente-agentOS.py
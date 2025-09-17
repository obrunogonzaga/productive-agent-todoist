FROM node:20-alpine

# deps básicas
RUN apk add --no-cache git
WORKDIR /app

# permite trocar o repositório via ARG/ENV
ARG AGENT_UI_REPO=https://github.com/agno-agi/agent-ui
RUN git clone --depth 1 ${AGENT_UI_REPO} .

# pnpm + build
ENV NEXT_TELEMETRY_DISABLED=1
RUN corepack enable && corepack prepare pnpm@latest --activate
RUN pnpm install --frozen-lockfile

# injeta o endpoint (build-time e runtime)
ARG NEXT_PUBLIC_DEFAULT_ENDPOINT
ENV NEXT_PUBLIC_DEFAULT_ENDPOINT=${NEXT_PUBLIC_DEFAULT_ENDPOINT}

RUN pnpm build
EXPOSE 3000
CMD ["pnpm", "start", "-p", "3000"]

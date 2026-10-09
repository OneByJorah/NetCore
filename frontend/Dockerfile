# =============================================================================
# NetCore Frontend — Next.js production image (standalone output)
#
# Previously this image ran `npm run dev`: a hot-reloading development server
# shipped as the production artifact. It now does a real production build and
# runs as a non-root user (trivy DS-0002).
#
# `next.config.js` sets `output: 'standalone'`, so the runtime image only needs
# the traced server bundle — not node_modules.
# =============================================================================

# ── Stage 1: dependencies ───────────────────────────────────────────────────
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci --prefer-offline

# ── Stage 2: build ──────────────────────────────────────────────────────────
FROM node:20-alpine AS builder
WORKDIR /app
ENV NEXT_TELEMETRY_DISABLED=1
COPY --from=deps /app/node_modules ./node_modules
COPY . .
# Next.js expects a public/ dir; this repo has none, so create an empty one to
# keep the standalone COPY below valid.
RUN mkdir -p public
RUN npm run build

# ── Stage 3: runtime ────────────────────────────────────────────────────────
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT=3000
ENV HOSTNAME=0.0.0.0

# Non-root: the node:alpine image already ships an unprivileged `node` user (uid 1000).
COPY --from=builder --chown=node:node /app/public ./public
COPY --from=builder --chown=node:node /app/.next/standalone ./
COPY --from=builder --chown=node:node /app/.next/static ./.next/static

USER node

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 --start-period=20s \
    CMD wget --spider -q http://127.0.0.1:3000/ || exit 1

CMD ["node", "server.js"]

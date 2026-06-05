# ── Stage 1: Build Tailwind CSS ──────────────────────────────
FROM node:20-slim AS css-builder

WORKDIR /app

# Install Node dependencies
COPY package.json ./
RUN npm install

# Copy source so Tailwind can scan for classes
COPY src/ ./src/

# Compile and minify Tailwind CSS
RUN npm run build

# ── Stage 2: Run Python App ───────────────────────────────────
FROM python:3.11-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy Python project files
COPY pyproject.toml ./
COPY src/ ./src/
COPY data/ ./data/

# Copy the compiled CSS from Stage 1
COPY --from=css-builder /app/src/dashboard/assets/styles.css ./src/dashboard/assets/styles.css

# Install Python dependencies using uv
RUN uv sync && uv pip install -e .

# Expose the port Dash runs on (default 8080)
EXPOSE 8080

# Run with Gunicorn
CMD ["uv", "run", "gunicorn", "dashboard.app:server", "-w", "2", "-b", "0.0.0.0:8080"]
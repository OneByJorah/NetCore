# =============================================================================
# NetCore Backend — FastAPI + Uvicorn
#
# No apt-get at all: every dependency in requirements.txt ships a prebuilt
# manylinux wheel, so no compiler is needed. This keeps the image small, makes
# builds hermetic, and avoids depending on the base image's apt mirror (which is
# inconsistent on this host: the index pins libssl3t64 u2 while u3 is offered,
# so installing libssl-dev fails outright).
# =============================================================================
FROM python:3.12-slim

WORKDIR /app

# Python dependencies (wheels only — no build toolchain required)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 netcore && chown -R netcore:netcore /app
USER netcore

EXPOSE 8000

# trivy DS-0026: healthcheck. Uses the bundled python so no curl/apt is needed.
HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=15s \
    CMD python -c "import urllib.request;urllib.request.urlopen('http://127.0.0.1:8000/health',timeout=5)" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

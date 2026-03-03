FROM astral/uv:python3.10-alpine3.23
ENV COIN=ADA
ENV PYTHONPATH=/app/src

WORKDIR /app

COPY pyproject.toml requirements.txt uv.lock ./

RUN uv pip install --no-cache-dir . --system

COPY src src

COPY config.yaml ./

CMD ["uv", "run", "python", "-m", "src.main"]

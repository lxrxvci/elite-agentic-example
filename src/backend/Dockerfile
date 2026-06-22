# Backend production Dockerfile
# Multi-stage build that installs only production dependencies and runs as a
# non-root user. Tests and dev dependencies are intentionally excluded from the
# final image.

FROM python:3.12-slim AS builder

WORKDIR /app

COPY pyproject.toml ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --user .

FROM python:3.12-slim AS production

WORKDIR /app

COPY --from=builder /root/.local /home/app/.local
COPY src ./src

RUN groupadd -r app && useradd -r -g app app && chown -R app:app /app
USER app

ENV PYTHONPATH=/app/src
ENV PATH=/home/app/.local/bin:$PATH
ENV PORT=8000
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

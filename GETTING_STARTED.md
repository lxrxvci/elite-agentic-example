# Getting Started

## Prerequisites

- Python 3.11+
- Node.js 20+
- Docker + docker-compose (for PostgreSQL)
- (Optional) Terraform 1.5+ for infrastructure

## 1. Environment setup

Copy the example environment file and fill in real values:

```bash
cp .env.example .env
```

Edit `.env`:
- `SECRET_KEY` — generate a strong random secret for production.
- `DATABASE_URL` — defaults to the Docker Compose PostgreSQL.
- `ALLOWED_ORIGINS` — update for your frontend URL.

## 2. Start PostgreSQL

```bash
docker-compose up -d postgres
```

## 3. Backend setup

```bash
cd src/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
alembic upgrade head
```

Run backend tests:

```bash
pytest
```

Start the backend:

```bash
uvicorn main:app --reload --port 8000
```

## 4. Frontend setup

```bash
cd src/frontend
npm install
```

Run frontend tests:

```bash
npm run test:ci
npm run test:a11y
```

Start the frontend:

```bash
npm run dev
```

## 5. Run the full stack

```bash
docker-compose up --build
```

The app will be available at `http://localhost:3000`.

## 6. Next steps

- Review `NORTH_STAR.md`, `PRODUCT_STRATEGY.md`, and `ROADMAP.md`.
- Inspect `docs/THREAT_MODEL.md` and `docs/SLOs.md`.
- Run the orchestrator: `python pipeline/orchestrator.py --project-dir . run`.

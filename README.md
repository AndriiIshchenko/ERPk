# ERPk
[![CI](https://github.com/AndriiIshchenko/ERPk/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/AndriiIshchenko/ERPk/actions/workflows/ci.yml)

A full-stack order management system built with FastAPI and React.

## Features

- **Authentication** — JWT-based register/login; all API routes are protected
- **Customers** — full CRUD
- **Products** — CRUD with soft-delete lifecycle (deactivate / restore) and full audit history
- **Orders** — Draft → Pending → Paid workflow; items can be added or removed while in draft

## Tech stack

| Layer | Technology |
|---|---|
| API | FastAPI, Python 3.13, Uvicorn |
| Database | PostgreSQL 16, SQLAlchemy 2 (async), asyncpg |
| Migrations | Alembic |
| Auth | JWT (python-jose), bcrypt (passlib) |
| Frontend | React 18, TypeScript, Vite |
| State / data | TanStack React Query v5, Axios |
| Routing | React Router v6 |
| Infrastructure | Docker, Docker Compose |

## Getting started

### Prerequisites

- Docker and Docker Compose

### 1. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and set a strong `SECRET_KEY`:

```bash
# generate a random key
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### 2. Start all services

```bash
docker-compose up -d
```

| Service | URL |
|---|---|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API docs (Swagger) | http://localhost:8000/docs |
| Adminer (DB GUI) | http://localhost:8080 |

### 3. Stop

```bash
docker-compose down
```

## Local development (without Docker)

### Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Running tests

Tests use `pytest-asyncio` and `httpx.AsyncClient` against a real PostgreSQL test database. Start the database first:

```bash
docker-compose up -d db
```

Then run the suite:

```bash
cd backend
pytest                        # all tests
pytest tests/test_orders.py   # single file
pytest -k "test_create_order" # single test
pytest --cov=app              # with coverage
```

## API overview

All endpoints are prefixed with `/api/v1/`. All routes except `/auth/*` require `Authorization: Bearer <token>`.

### Auth

| Method | Endpoint | Description | Success |
|---|---|---|---|
| `POST` | `/auth/register` | Create a new user account and return a JWT | `201` |
| `POST` | `/auth/login` | Authenticate with email + password and return a JWT | `200` |

### Customers

| Method | Endpoint | Description | Success |
|---|---|---|---|
| `GET` | `/customers` | List all customers | `200` |
| `GET` | `/customers/{id}` | Get a single customer by ID | `200` |
| `POST` | `/customers` | Create a new customer; `409` if email already exists | `201` |
| `PUT` | `/customers/{id}` | Update customer fields (all optional); `409` on duplicate email | `200` |
| `DELETE` | `/customers/{id}` | Hard-delete a customer | `204` |

### Products

| Method | Endpoint | Description | Success |
|---|---|---|---|
| `GET` | `/products` | List active products; add `?include_inactive=true` to include deactivated ones | `200` |
| `GET` | `/products/{id}` | Get a single product by ID | `200` |
| `GET` | `/products/{id}/history` | Get the full audit log for a product, newest entry first | `200` |
| `POST` | `/products` | Create a new active product | `201` |
| `PUT` | `/products/{id}` | Update product fields; `409` if product is inactive | `200` |
| `POST` | `/products/{id}/deactivate` | Soft-delete a product; `409` if already inactive | `200` |
| `POST` | `/products/{id}/restore` | Re-activate a deactivated product; `409` if already active | `200` |

### Orders

Orders follow a strict lifecycle: **draft → pending → paid**. Items can only be modified while the order is in `draft` status.

| Method | Endpoint | Description | Success |
|---|---|---|---|
| `GET` | `/orders` | List all orders | `200` |
| `GET` | `/orders/{id}` | Get a single order with its items | `200` |
| `GET` | `/orders/customer/{customer_id}` | List all orders for a specific customer | `200` |
| `POST` | `/orders` | Create an empty draft order for an existing customer | `201` |
| `POST` | `/orders/{id}/items` | Add a product to a draft order; `409` if already present or order is not draft | `200` |
| `DELETE` | `/orders/{id}/items/{item_id}` | Remove a line item from a draft order | `200` |
| `POST` | `/orders/{id}/confirm` | Confirm a draft order (moves to `pending`); `422` if order has no items | `200` |
| `POST` | `/orders/{id}/pay` | Mark a pending order as paid; `409` if order is not pending | `200` |
| `POST` | `/orders/{id}/cancel` | Cancel a draft or pending order; `409` if already paid or cancelled | `200` |
| `DELETE` | `/orders/{id}` | Hard-delete an order and all its items | `204` |

## Project structure

```
ERPk/
├── backend/
│   ├── app/
│   │   ├── api/v1/        # Route handlers
│   │   ├── core/          # Config, database, security
│   │   ├── models/        # SQLAlchemy ORM models
│   │   ├── repositories/  # Database query layer
│   │   ├── schemas/       # Pydantic request/response schemas
│   │   └── services/      # Business logic layer
│   ├── alembic/           # Database migrations
│   └── tests/
├── frontend/
│   └── src/
│       ├── api/           # Axios client functions
│       ├── hooks/         # React Query hooks
│       ├── pages/         # Page components
│       ├── components/    # Shared UI components
│       └── types/         # TypeScript interfaces
├── docker-compose.yml
└── .env.example
```

## Architecture

The backend follows a strict 4-layer pattern: **routes → services → repositories → ORM**. Business rules live exclusively in services; routes handle only HTTP concerns; repositories handle only DB queries.

Key design decisions:

- **Price snapshot** — `OrderItem.price_snapshot` copies the product price at the time of adding an item. Editing a product never retroactively changes order totals.
- **Soft delete** — Products are deactivated (not deleted), preserving order history integrity.

## Environment variables

| Variable | Description |
|---|---|
| `POSTGRES_USER` | PostgreSQL username |
| `POSTGRES_PASSWORD` | PostgreSQL password |
| `POSTGRES_DB` | PostgreSQL database name |
| `DATABASE_URL` | Full asyncpg connection string |
| `SECRET_KEY` | JWT signing secret (min 32 bytes) |
| `ALGORITHM` | JWT algorithm (default: `HS256`) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime (default: `30`) |
| `VITE_API_URL` | Backend URL used by the frontend |


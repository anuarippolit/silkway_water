# Water CRM

Internal order management system for a water delivery business.

Workers create and manage customer orders, while couriers update delivery statuses. The project provides a REST API built with FastAPI and PostgreSQL.

---

## Tech Stack

Python 3.13 - FastAPI - PostgreSQL - SQLAlchemy 2.0 (Async) - Alembic - Docker

---

## Getting Started

1. Clone the repository

```bash
git clone https://github.com/your_username/water-crm.git
cd water-crm
```

2. Create a virtual environment

Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Configure the following variables inside `.env`:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5433/watercrm

BOT_TOKEN=your_telegram_bot_token
```

---

## Running PostgreSQL

Start PostgreSQL using Docker:

```bash
docker run --name water-db \
    -e POSTGRES_USER=user \
    -e POSTGRES_PASSWORD=password \
    -e POSTGRES_DB=watercrm \
    -p 5433:5432 \
    -d postgres:16
```

---

## Database Migration

Apply Alembic migrations:

```bash
alembic upgrade head
```

---

## Running the Server

Start the development server:

```bash
uvicorn app.main:app --reload
```

The application will be available at:

```
http://localhost:8000
```

Swagger documentation:

```
http://localhost:8000/docs
```

---

## Project Structure

```
app/
│
├── api/
│   └── routers/          # HTTP endpoints
│
├── core/                 # Configuration, database, security
│
├── models/               # SQLAlchemy models
│
├── schemas/              # Pydantic schemas
│
├── services/             # Business logic
│
├── dependencies.py       # Authentication dependencies
│
└── main.py               # FastAPI application
```

---

## Example API Request

### Create Order

```http
POST /orders/
```

#### Headers

```http
Content-Type: application/json
init-data: <telegram_init_data>
```

#### Request Body

```json
{
  "phone": "87078507506",
  "address": "Seifullin 33",
  "name": "John Doe",
  "bottles_qty": 3,
  "bottle_price": 1400,
  "bottle_condition": "new",
  "payment_status": "unpaid",
  "order_status": "actual",
  "delivery_date": "2026-06-20",
  "addons": []
}
```

#### cURL

```bash
curl -X POST http://localhost:8000/orders/ \
  -H "Content-Type: application/json" \
  -H "init-data: <telegram_init_data>" \
  -d '{
    "phone": "87078507506",
    "address": "Seifullin 33",
    "name": "John Doe",
    "bottles_qty": 3,
    "bottle_price": 1400,
    "bottle_condition": "new",
    "payment_status": "unpaid",
    "order_status": "actual",
    "delivery_date": "2026-06-20",
    "addons": []
  }'
```

#### Response

```json
{
  "id": "d3115475-47f2-4722-98f9-a93333d550c2",
  "contact": {
    "id": "00b5b3c0-3531-4b4b-b878-bd3deb860d1c",
    "name": "John Doe",
    "address": "Seifullin 33",
    "phone": "87078507506"
  },
  "bottles_qty": 3,
  "bottle_price": 1400,
  "total_amount": 4200,
  "order_status": "actual",
  "payment_status": "unpaid",
  "delivery_date": "2026-06-20",
  "addons": []
}
```

---

## Features

- REST API built with FastAPI
- Async SQLAlchemy 2.0
- PostgreSQL database
- Alembic migrations
- Telegram Mini App authentication
- Order management
- Contact management
- Delivery status tracking
- Interactive Swagger documentation

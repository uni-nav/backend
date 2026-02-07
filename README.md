# University Navigation System — Backend (FastAPI)

Bu servis bino ichida navigatsiya (qavat → waypoint → connection → pathfinding) uchun API beradi.

## Talablar

- Docker Desktop + Docker Compose v2
- `make` (ixtiyoriy, lekin qulay)

Agar Docker ishlatmasangiz:
- Python 3.11+
- PostgreSQL 15+

## Tezkor Boshlash

### 1) `.env` tayyorlang

```bash
cd bino_xarita_admin
cp .env.example .env
```

**Production'da albatta o'zgartiring:**
- `SECRET_KEY` (kamida 32 belgi)
- `JWT_SECRET_KEY` (kamida 32 belgi, `SECRET_KEY` dan farqli)
- `ADMIN_TOKEN` (kamida 32 belgi)
- `ALLOWED_ORIGINS` (prod'da `*` bo'lmasin)
- `ENV=production`

### 2) Frontend nomi

Agar frontend Git'dan boshqa nom bilan tushgan bo'lsa, `.env` da o'zgartiring:

```bash
# GitHub: https://github.com/uni-nav/campus-navigator-1
FRONTEND_DIR=campus-navigator-1
```

### 3) Portlarni sozlash

```bash
# .env da:
API_PORT=8000
FRONTEND_PORT=8080
```

### 4) Ishga tushirish

```bash
# Development
make dev-d
make migrate
make test

# Production
make prod
make migrate
```

## Kirish manzillari

| Servis | URL |
|--------|-----|
| API | `http://localhost:${API_PORT}` |
| Swagger | `http://localhost:${API_PORT}/docs` |
| Frontend | `http://localhost:${FRONTEND_PORT}` |

## Admin autentifikatsiya

Admin endpointlar uchun header:
```
Authorization: Bearer <ADMIN_TOKEN>
```

JWT login: `/api/auth/login`

## Asosiy komandalar

```bash
make dev        # Development (attached)
make dev-d      # Development (detached)
make prod       # Production
make stop       # To'xtatish
make migrate    # Database migrations
make test       # Testlarni ishlatish
make logs       # Loglarni ko'rish
make backup-db  # Database backup
make help       # Barcha komandalar
```

## Troubleshooting

DB xatolari (Docker volume eski bo'lsa):
```bash
make reset-db
make dev-d
make migrate
```

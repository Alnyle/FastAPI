Redis is an excellent addition to a FastAPI application. It's commonly used for caching, rate limiting, sessions, background jobs, and pub/sub messaging.

Since you're already using PostgreSQL in Docker, the typical architecture becomes:

```text
                 +------------------+
                 |   FastAPI App    |
                 +--------+---------+
                          |
          +---------------+---------------+
          |                               |
          v                               v
+---------------------+          +-----------------+
| PostgreSQL          |          | Redis           |
| Persistent Storage  |          | In-Memory Store |
+---------------------+          +-----------------+
```

## Add Redis to Docker Compose

Extend your `docker-compose.yml`:

```yaml
services:
  postgres:
    image: postgres:17
    container_name: fastapi_postgres

    restart: always

    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: fastapi_db

    ports:
      - "5432:5432"

    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:8
    container_name: fastapi_redis

    restart: always

    ports:
      - "6379:6379"

    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

Start everything:

```bash
docker compose up -d
```

Check that both are running:

```bash
docker ps
```

You should see both PostgreSQL and Redis containers.

---

## Install the Redis client

For async FastAPI:

```bash
pip install redis
```

The modern `redis` package includes asyncio support, so you don't need the old `aioredis` package.

---

## Connect to Redis

Create `database/redis.py`:

```python
from redis.asyncio import Redis

redis = Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
)
```

If your FastAPI app later runs inside Docker too, change:

```python
host="redis"
```

because `redis` is the service name in Docker Compose.

---

## Test it

```python
from database.redis import redis

await redis.set("username", "Ahmed")

name = await redis.get("username")

print(name)
```

Output:

```text
Ahmed
```

---

# Common use cases

### 1. Cache expensive database queries

Instead of querying PostgreSQL every request:

```python
user = await redis.get(f"user:{user_id}")

if user is None:
    user = await load_user_from_database(user_id)
    await redis.set(f"user:{user_id}", user, ex=300)
```

This caches the result for 5 minutes.

---

### 2. Store JWT access token blocklists

When a user logs out:

```python
await redis.set(
    f"blacklist:{jti}",
    "1",
    ex=3600,
)
```

Then check Redis on every authenticated request to reject revoked tokens.

---

### 3. Rate limiting

Example:

```text
ip:192.168.1.5 -> 42 requests
```

Redis can increment counters very quickly.

---

### 4. OTP verification

```text
otp:email@gmail.com -> 823517
```

Expire automatically after a few minutes.

---

### 5. Background jobs

Libraries like Celery, RQ, or Arq often use Redis as a message broker.

---

## Project structure

```text
app/
│
├── api/
├── database/
│   ├── postgres.py
│   └── redis.py
├── models/
├── services/
├── routers/
├── core/
└── main.py
```

## For your project

Based on your recent FastAPI work (JWT authentication, sellers, and the AI healthcare blog backend), Redis would be especially useful for:

* **JWT token revocation (blacklist)**
* **Caching frequently accessed blog posts**
* **Rate limiting API endpoints**
* **Caching expensive database queries**
* **Email verification or password reset codes** (if you add authentication later)

This combination—**FastAPI + PostgreSQL + Redis + SQLAlchemy (async) + Alembic**—is a solid, production-ready backend stack that you'll encounter in many real-world applications.

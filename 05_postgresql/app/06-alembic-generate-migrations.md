 Those commands look correct for a **uv-managed** project. Here's what they do and how to use them properly:

## The Commands Explained

```bash
# 1. Generate an initial migration from your SQLAlchemy models
uv run alembic revision --autogenerate -m "init"

# 2. Apply all pending migrations to the database
uv run alembic upgrade head
```

`uv run` ensures Alembic runs inside your project's virtual environment without you manually activating it.

---

## Prerequisites (uv project)

Make sure your `pyproject.toml` includes Alembic and your database driver:

```toml
[project]
dependencies = [
    "fastapi",
    "sqlalchemy",
    "alembic",
    "psycopg2-binary",  # or "asyncpg" / "pymysql" / etc.
]
```

And that you've initialized Alembic first:

```bash
uv run alembic init alembic
```

---

## Typical Workflow

```bash
# After changing your SQLAlchemy models:
uv run alembic revision --autogenerate -m "add posts table"

# Review the generated file in alembic/versions/ before applying!

# Apply it:
uv run alembic upgrade head

# Check current state:
uv run alembic current

# Rollback one migration (if needed):
uv run alembic downgrade -1
```

---

## Common Gotchas

| Issue | Fix |
|-------|-----|
| **"Can't locate revision identified by '...'"** | Your database has a migration applied that no longer exists in `alembic/versions/`. Run `uv run alembic stamp head` to reset, or restore the missing file. |
| **Autogenerate produces empty migration** | Make sure `target_metadata = Base.metadata` is set in `alembic/env.py` and your models are imported there. |
| **Module not found errors** | Ensure your project root is in `PYTHONPATH`. In `alembic/env.py`, add: `sys.path.append(os.path.dirname(os.path.dirname(__file__)))` |
| **Database URL not found** | Set `DATABASE_URL` in your environment, or read from `.env` in `alembic/env.py` using `os.getenv`. |

---

## Pro Tip: Add uv Scripts

Add shortcuts to your `pyproject.toml` so you don't type the full commands every time:

```toml
[tool.uv.pip]
# (uv doesn't have scripts like npm, but you can use task runners)

# Or use a Makefile / justfile:
```

Or use a `justfile`:

```just
migrate:
    uv run alembic revision --autogenerate -m "{{msg}}"

upgrade:
    uv run alembic upgrade head

downgrade:
    uv run alembic downgrade -1
```

Then: `just migrate msg="add users table"`

---

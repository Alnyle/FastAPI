from fastapi import FastAPI
from models import Base
from database import engine
from routers import auth, todos

app = FastAPI()


# .schema : show you all the tables thate currently within our sqlite database

# When the app starts, it ensures all tables (defined in models.py) are created in your database (todos.db).
# It won’t drop or overwrite — it just creates missing tables.
Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(todos.router)



# 
# {
#   "title": "Watch golab tutorial",
#   "description": "learn to use golab power from GPU and RAM",
#   "priority": 2,
#   "complete": False
# }
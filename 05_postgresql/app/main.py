from contextlib import asynccontextmanager
from fastapi import FastAPI
from database.session import create_db_tables
from api.router import master_router as router
from scalar_fastapi import get_scalar_api_reference

# from rich import print, panel




@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    
    # print(panel.Panel("Serve start...", title="Lifespan", style="bold green"))
    await create_db_tables()
    yield
    # print(panel.Panel("Serve stop...", title="Lifespan", style="bold red"))

app = FastAPI(
    lifespan=lifespan_handler,
    docs_url=None,  # Disable Swagger UI (optional)
    redoc_url=None, # Disable ReDoc (optional)
)

@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="My API",
    )

app.include_router(router=router)



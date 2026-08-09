If you mean **Scalar API Reference** (the modern API documentation UI) for a FastAPI project, you can easily replace or add it alongside Swagger UI.

### 1. Install Scalar support

```bash
pip install scalar-fastapi
```

### 2. Configure FastAPI

```python
from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

app = FastAPI(
    docs_url=None,      # Disable Swagger UI (optional)
    redoc_url=None,     # Disable ReDoc (optional)
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="My API",
    )
```

Now visit:

```
http://127.0.0.1:8000/scalar
```

---

### 3. Keep Swagger as well (optional)

If you want both Swagger and Scalar:

```python
app = FastAPI()

@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="My API",
    )
```

Then you'll have:

* Swagger UI → `http://127.0.0.1:8000/docs`
* ReDoc → `http://127.0.0.1:8000/redoc`
* Scalar → `http://127.0.0.1:8000/scalar`

---

### Why many developers prefer Scalar

* Cleaner and more modern interface.
* Better API exploration experience.
* Excellent dark mode.
* Supports authentication (Bearer tokens, API keys).
* Generates code snippets for multiple languages.
* Handles large APIs more smoothly than Swagger UI.

For a production FastAPI backend, it's common to expose only **Scalar** (or Swagger) and disable the others if you don't need multiple documentation UIs.

**You:**

query parameters in fastapi explain

* * *

**ChatGPT:**

Got it 👍 let’s break **query parameters in FastAPI** step by step.

* * *

🔹 What are Query Parameters?
-----------------------------

Query parameters are values passed in the **URL after the `?` symbol**, usually used for filtering, searching, sorting, or providing optional data.

Example URL:

```
http://127.0.0.1:8000/items?skip=10&limit=5
```

Here:

* `skip=10` → query parameter
    
* `limit=5` → query parameter
    

* * *

🔹 Declaring Query Parameters in FastAPI
----------------------------------------

You just add them as **function parameters** in your path operation.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

* `skip` and `limit` will be taken from the query string.
    
* If they are not provided, defaults (`0` and `10`) are used.
    

* * *

🔹 Required Query Parameters
----------------------------

If you don’t set a default value, the parameter becomes **required**.

```python
@app.get("/users/")
def read_users(name: str):
    return {"user": name}
```

Request:

```
http://127.0.0.1:8000/users?name=Ahmed
```

If you don’t pass `name`, FastAPI will return a **validation error**.

* * *

🔹 Optional Query Parameters
----------------------------

You can use **`Optional`** from `typing` for better readability.

```python
from typing import Optional

@app.get("/search/")
def search_items(q: Optional[str] = None):
    return {"query": q}
```

Now `/search?q=book` → returns `{"query": "book"}`  
And `/search` → returns `{"query": null}`

* * *

🔹 Multiple Query Parameters
----------------------------

You can have as many as you want:

```python
@app.get("/filter/")
def filter_items(category: str, price: float, available: bool = True):
    return {"category": category, "price": price, "available": available}
```

Request:

```
http://127.0.0.1:8000/filter?category=shoes&price=199.99&available=false
```

* * *

🔹 Advanced: Validation with `Query`
------------------------------------

FastAPI provides `Query` for more control (validation, metadata, etc.):

```python
from fastapi import Query

@app.get("/items/")
def read_items(q: str = Query(..., min_length=3, max_length=50)):
    return {"query": q}
```

* `...` means required
    
* `min_length=3` → string must have at least 3 characters
    
* `max_length=50` → string must have at most 50 characters
    

Example:

```
http://127.0.0.1:8000/items?q=abc
```

* * *

✅ Summary:

* Query params = come after `?` in the URL.
    
* With defaults → optional.
    
* Without defaults → required.
    
* Use `Query()` for validation and metadata.
    

* * *

Do you want me to also explain **the difference between path parameters and query parameters** (since people often mix them up)?
**ChatGPT:**

Great question 👌

In **FastAPI**, a `PUT` request is typically used to **update an existing resource** (like updating a user’s info).

The main difference from `POST`:

* **POST** → create a new resource (can be multiple new entries).
    
* **PUT** → update an existing resource (idempotent: same request repeated won’t create duplicates).
    

* * *

### Example: Update a User with `PUT`

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Request body schema
class User(BaseModel):
    username: str
    email: str
    age: int

# Mock database
fake_db = {
    1: {"username": "ahmed", "email": "ahmed@example.com", "age": 23}
}

@app.put("/users/{user_id}")
async def update_user(user_id: int, user: User):
    if user_id not in fake_db:
        return {"error": "User not found"}
    
    # Update user
    fake_db[user_id] = user.dict()
    return {"message": "User updated successfully", "user": fake_db[user_id]}
```

* * *

### Request (using `curl` or Postman)

```bash
curl -X PUT "http://127.0.0.1:8000/users/1" \
     -H "Content-Type: application/json" \
     -d '{"username": "ahmed_new", "email": "new@example.com", "age": 25}'
```

### Response

```json
{
  "message": "User updated successfully",
  "user": {
    "username": "ahmed_new",
    "email": "new@example.com",
    "age": 25
  }
}
```

* * *

### 🔑 Key Points

* `PUT` usually replaces the **whole resource** with new data.
    
* If you only want to **partially update** a resource (like just changing the `age`), you should use **PATCH** instead.
    

* * *

👉 Do you want me to also show you the **PATCH request** example (partial update) for comparison?
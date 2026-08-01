**You:**

passlib abd bcrypt in fastapi

* * *

**ChatGPT:**

Got it 👍 You want to understand how to use **Passlib** and **bcrypt** with **FastAPI** for handling password hashing and verification.

Here’s a breakdown and example:

* * *

🔑 Why use Passlib + bcrypt?
----------------------------

* **bcrypt** is a secure hashing algorithm designed for passwords.
    
* **Passlib** is a Python library that wraps bcrypt and other hashing algorithms, making it **easy and safe** to hash, verify, and upgrade passwords over time.
    
* In **FastAPI**, we use it to store only hashed passwords in the database (never plain text).
    

* * *

⚙️ Setup
--------

Install required packages:

```bash
pip install passlib[bcrypt] fastapi uvicorn
```

* * *

📝 Example with Passlib + bcrypt in FastAPI
-------------------------------------------

```python
from fastapi import FastAPI, Depends, HTTPException
from passlib.context import CryptContext
from pydantic import BaseModel

app = FastAPI()

# Setup Passlib context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Fake "DB" for demo
fake_users_db = {}

# Schema for user input
class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

# Hashing helpers
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@app.post("/register")
def register(user: UserCreate):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    hashed_pw = hash_password(user.password)
    fake_users_db[user.username] = {"username": user.username, "password": hashed_pw}
    return {"msg": "User registered successfully!"}

@app.post("/login")
def login(user: UserLogin):
    db_user = fake_users_db.get(user.username)
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"msg": f"Welcome {user.username}!"}
```

* * *

🚀 How it works
---------------

1. **Register**:
    
    * Takes username + password
        
    * Hashes password with **bcrypt via Passlib**
        
    * Stores hashed password in DB
        
2. **Login**:
    
    * Fetches stored hashed password from DB
        
    * Uses `verify_password()` to check plain password against hash
        

* * *

✅ Secure: Passwords are never stored in plain text.  
✅ Easy: Passlib manages bcrypt safely and can switch algorithms later.  
✅ Standard practice in FastAPI apps (usually combined with JWT for authentication).

* * *

Do you want me to also show you how to integrate this with **JWT authentication** (so you can create login tokens), or just password hashing/verification for now?
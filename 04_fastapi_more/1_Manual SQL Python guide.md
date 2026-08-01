**You:**

# will work without commit becuase it's a table operation
# cursor.execute("DROP TABLE shipment")

# shipment_data = [
#     (1231, 'sunscreen', 14.2, 'placed'),
#     (1232, 'beach chairs', 15.7, 'shipped'),
#     (1233, 'sunscreen', 2.1, 'delivered'),
#     (1234, 'surfboards', 22.5, 'placed'),
#     (1235, 'beach towels', 5.8, 'in transit'),
#     (1236, 'coolers', 12.3, 'placed'),
#     (1237, 'snorkel gear', 3.9, 'delivered')
# ]
# cursor.executemany("INSERT INTO shipment VALUES (?, ?, ?, ?)", shipment_data)
# connection.commit()

# Add shipment database 
# cursor.execute("""
#     INSERT INTO shipment VALUES (1231, 'sunscreen', 14.2, 'placed')
# """)




# commit the changes to the database 
# connection.commit()

# 2. Fetch a shipment using id
# cursor.execute("""
#     SELECT * FROM shipment 
# """)

# # res = cursor.fetchall()
# res = cursor.fetchmany(2) # fetch first two
# # res = cursor.fetchone() # fetch first item
# print(res)


# 3. Update our data
# cursor.execute("""
#     UPDATE shipment SET status = "in_transit"
#     WHERE status = "in transit"
# """)
# connection.commit()

# 4. Delete from shipment
# cursor.execute("""
#     DELETE FROM shipment WHERE id = 1231
# """)

# # commit the changes to the database 
# connection.commit()


## SQL query parameters ##
# id = 1236
# status = "placed"

# cursor.execute(f"""
#     UPDATE shipment SET status = '{status}'
#     WHERE id = {id}
# """)
# connection.commit()

# strict parameter order
# cursor.execute("""
#     UPDATE shipment SET status = ?
#     WHERE id = ?
# """, (id, status))
# connection.commit()

# as dictionary 
# cursor.execute("""
#     UPDATE shipment SET status = :status
#     WHERE id = :id
# """,
#     { "status": status, "id": id }
# )
# connection.commit()

# Close the connection when done
# connection.close()  .create guide from it

* * *

**ChatGPT:**

Got it 👍 You want me to create a **step-by-step guide** from your commented SQL/Python code so it’s clear and structured.  
Here’s a clean guide based on your code:

* * *

📘 SQLite Database Guide with Python
====================================

This guide walks through creating, inserting, updating, deleting, and querying a `shipment` table using Python’s `sqlite3` module.

* * *

1. Setup the Database Connection
--------------------------------

```python
import sqlite3

# Create or connect to a database
connection = sqlite3.connect("shipments.db")
cursor = connection.cursor()
```

* * *

2. Create the Shipment Table
----------------------------

```python
cursor.execute("""
CREATE TABLE IF NOT EXISTS shipment (
    id INTEGER PRIMARY KEY,
    product TEXT,
    weight REAL,
    status TEXT
)
""")
```

* * *

3. Insert Data
--------------

### Insert Multiple Rows

```python
shipment_data = [
    (1231, 'sunscreen', 14.2, 'placed'),
    (1232, 'beach chairs', 15.7, 'shipped'),
    (1233, 'sunscreen', 2.1, 'delivered'),
    (1234, 'surfboards', 22.5, 'placed'),
    (1235, 'beach towels', 5.8, 'in transit'),
    (1236, 'coolers', 12.3, 'placed'),
    (1237, 'snorkel gear', 3.9, 'delivered')
]

cursor.executemany("INSERT INTO shipment VALUES (?, ?, ?, ?)", shipment_data)
connection.commit()
```

### Insert a Single Row

```python
cursor.execute("""
INSERT INTO shipment VALUES (1238, 'umbrellas', 10.5, 'placed')
""")
connection.commit()
```

* * *

4. Fetch Data
-------------

### Fetch All

```python
cursor.execute("SELECT * FROM shipment")
res = cursor.fetchall()
print(res)
```

### Fetch First N Rows

```python
cursor.execute("SELECT * FROM shipment")
res = cursor.fetchmany(2)  # first 2 rows
print(res)
```

### Fetch One Row

```python
cursor.execute("SELECT * FROM shipment")
res = cursor.fetchone()
print(res)
```

* * *

5. Update Data
--------------

### Simple Update

```python
cursor.execute("""
UPDATE shipment SET status = "in_transit"
WHERE status = "in transit"
""")
connection.commit()
```

### Update Using Variables (String Formatting) ⚠️ Not safe

```python
id = 1236
status = "placed"

cursor.execute(f"""
UPDATE shipment SET status = '{status}'
WHERE id = {id}
""")
connection.commit()
```

### Update Using Parameters (Safe Way ✅)

#### Positional Parameters

```python
cursor.execute("""
UPDATE shipment SET status = ?
WHERE id = ?
""", (status, id))
connection.commit()
```

#### Named Parameters

```python
cursor.execute("""
UPDATE shipment SET status = :status
WHERE id = :id
""", {"status": status, "id": id})
connection.commit()
```

* * *

6. Delete Data
--------------

```python
cursor.execute("DELETE FROM shipment WHERE id = 1231")
connection.commit()
```

* * *

7. Drop Table
-------------

```python
cursor.execute("DROP TABLE shipment")
```

⚠️ Dropping a table does **not require `commit()`**, but changes won’t persist until committed if in a transaction.

* * *

8. Close Connection
-------------------

```python
connection.close()
```

* * *

✅ This guide covers **all CRUD operations** (Create, Read, Update, Delete) + safe parameterized queries for SQL injection prevention.

Do you want me to also add **best practices** (like always using `with sqlite3.connect(...) as conn:` context manager) to make it more professional?
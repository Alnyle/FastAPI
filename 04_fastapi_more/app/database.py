import sqlite3
from schemas import ShipmentCreate, ShipmentUpdate
from typing import Any

# Create method that expose methods to operate (comunciate) with database (read, create, delete, update)
class Database:
    
    def conntect_to_db(self):
        
        # Make connection with database 
        self.conn = sqlite3.connect("sqlite.db", check_same_thread=False)
        # Get cursor to execute quries and fetch data : to execute our queries throgh it
        self.cur = self.conn.cursor()
        
    def create_table(self):
        # 1. Create a table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS shipment (
                id INTEGER PRIMARY KEY, 
                content TEXT, 
                weight REAL, 
                status TEXT
            )
        """)
        

        
    def create(self, shipment: ShipmentCreate) -> int:
        # Find a new id
        self.cur.execute("SELECT MAX(id) FROM shipment")
        result = self.cur.fetchone()
        if result[0] is None:
            mx = 0
        else :
            mx = result[0]
            
        new_id = mx + 1
        self.cur.execute("""
            INSERT INTO shipment VALUES (:id, :content, :weight, :status)
        """,
            {
                "id": new_id,
                **shipment.model_dump(),
                "status": "placed",
            }
        )
        self.conn.commit()
        return new_id
        
    def get(self, id: int) -> dict[str, Any] | None:
        
        self.cur.execute("""
            SELECT * FROM shipment WHERE id = ?
        """, (id,))        
        row = self.cur.fetchone()
        
        return { 
                "id": row[0],
                "content": row[1], 
                "weight": row[2], 
                "status": row[3],
            } if row else None
    
    def update(self, id: int, shipment: ShipmentUpdate) -> dict[str, Any]:
        
        self.cur.execute("""
            UPDATE shipment SET status = :status
            WHERE id = :id
        """,
            {
                "id": id,
                **shipment.model_dump()
            }
        )
        self.conn.commit()
        
        return self.get(id)
    
    def delete(self, id: int):
        
        self.cur.execute("""
            DELETE FROM shipment WHERE id = ?
        """, (id,))
        
        self.conn.commit()

    def delete_all(self):
        self.cur.execute("DELETE FROM shipment")
        self.conn.commit()

    def close(self):
        
        self.conn.close()
    
    def __enter__(self):
        self.conntect_to_db()
        
    def __exist__(self, *args):
        self.close()
# context manger methods
# Usage 
# db = Database()

with Database as db:
    db.get(1)
    db.get(1)
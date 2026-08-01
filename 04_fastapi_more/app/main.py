from fastapi import FastAPI, HTTPException, status
from schemas import ShipmentCreate, ShipmentUpdate, ShipmentRead
from database import Database
from typing import Any

app = FastAPI()

db = Database()

@app.get('/shipment/{id}', response_model=ShipmentRead)
async def get_shipment(id: int):
    
    shipment = db.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Give id does not exist!",
        )
        
    return shipment



@app.post('/shipment/', response_model=dict)
async def sumbit_shipment(shipment: ShipmentCreate) -> dict[str, Any]:
    
    new_id = db.create(shipment)
    
    return {"details": f"Shipment with id #{new_id} is created"}


@app.patch('/shipment/{id}')
async def update_shipment(id: int, shipment: ShipmentUpdate):
    
    updated_shipment = db.update(id, shipment)
    
    return updated_shipment


@app.delete('/shipment/{id}')
async def delete_shipment(id: int):
    
    db.delete(id)
    
    return {"details": f"Shipment with id #{id} is delete"}


@app.get("/shipment/delete_all")
async def delete_all_shipments():
    
    db.delete_all()
    
    return {"details": "All shipments are deleted"}
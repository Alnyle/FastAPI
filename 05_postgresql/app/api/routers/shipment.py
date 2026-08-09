from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from api.schemas.shipment import Shipment, ShipmentUpdate, ShipmentCreate
from api.dependencies import ActiveSellerDep, DeliveryPartnerDep, DeliveryPartnerServiceDep, ShipmentServiceDep


router = APIRouter(prefix="/shioment", tags=["Shipment"])




@router.get('/', response_model=Shipment)
async def get_shipment(
    id: UUID, 
    service: ShipmentServiceDep,
    _ : ActiveSellerDep,
):

    shipment = await service.get(id)


    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Give id does't exist!" 
        )

    return shipment



@router.post('/')
async def sumbit_shipment(
    seller: ActiveSellerDep,
    shipment: ShipmentCreate,
    service: ShipmentServiceDep,
) -> Shipment:

    shipment = await service.add(shipment, seller)
    # return {"details": f"Shipment with id #{new_shipment.id} is created"}
    return shipment


@router.patch('/{id}', response_model=Shipment)
async def update_shipment(
    id: UUID,
    shipment_update: ShipmentUpdate,
    partner: DeliveryPartnerDep,
    service: ShipmentServiceDep
):

            # exclude the none fields
    update = shipment_update.model_dump(exclude_none=True)
    print(update)
    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided to update",
        )

    #  Validate logged in partner with assgined partner
    # on the shipment with given id
    shipment = await service.get(id)

    if shipment.delivery_partner_id != partner.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized"
        )

    shipment = await service.update(
        shipment.sqlmodel_update(shipment_update)
    )
    return shipment


@router.delete('/')
async def delete_shipment(id: UUID, service: ShipmentServiceDep):

    await service.delete(id)
    return {"details": f"Shipment with id #{id} is delete"}

# @app.get("/shipment/delete_all")
# async def delete_all_shipments(session: SessionDep):
    
#     session.exec(Shipment).delete()
#     session.commit()
#     return {"details": "All shipments are deleted"}


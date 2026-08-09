from uuid import UUID

from fastapi import status
from api.schemas.shipment import Shipment, ShipmentCreate, ShipmentUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from database.models import Seller, ShipmentStatus
from datetime import datetime, timedelta
from .base import BaseService
from .delivery_partner import DeliveryPartnerService

class ShipmentService(BaseService):

    def __init__(
        self, 
        session: AsyncSession,
        partner_service: DeliveryPartnerService
    ):

        # Initialize the session through parent class
        super().__init__(Shipment, session)
        self.partner_service = partner_service



    async def get(self, id: UUID) -> Shipment | None:
        return await self._get(id)


    async def add(self, shipment_create: ShipmentCreate, seller: Seller) -> Shipment:


        new_shipment = Shipment(
            **shipment_create.model_dump(),
            status=ShipmentStatus.placed,
            estimated_delivery=datetime.now() + timedelta(days=3),
            seller_id=seller.id,
        )

        # add a new shipment
        partner = await self.partner_service.assign_shipment(new_shipment)
        # assign a shipment a delivery partner 
        new_shipment.delivery_partner_id = partner.id
        shipment = await self._add(new_shipment)
        return shipment


        
    async def update(self, shipment: Shipment) -> Shipment:
        return await self._update(shipment)
        
    async def delete(self, id: int) -> None:

        await self._delete(await self.get(id))

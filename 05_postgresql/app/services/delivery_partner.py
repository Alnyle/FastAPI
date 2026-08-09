

from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select, any_

from api.schemas.delivery_partner import DeliveryPartnerCreate
from api.schemas.shipment import Shipment
from database.models import DeliveryPartner
from services.user import UserService


class DeliveryPartnerService(UserService):

    def __init__(self, session):
        super().__init__(DeliveryPartner, session)


    async def add (self, delivery_partner: DeliveryPartnerCreate):

        return await self._add_user(
            delivery_partner.model_dump(),
        )


    async def get_partners_by_zipcode(self, zipcode: int) -> Sequence[DeliveryPartner]:
        result = await self.session.scalars(
            select(DeliveryPartner).where(
                zipcode == any_(DeliveryPartner.serviceable_zip_codes)
            )
        )

        return result.all()


    async def assign_shipment(self, shipment: Shipment):

        eligiable_partners = await self.get_partners_by_zipcode(shipment.destination)

        for partner in eligiable_partners:
            if partner.current_handling_capacity() > 0:
                partner.shipments.append(shipment)
                return partner

        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="No delivery partner is available"
        )
    
    async def update(self, partner: DeliveryPartner):
        return await self._update(partner)

    async def token(self, email, password):

        return await self._generate_token(email=email, password=password)
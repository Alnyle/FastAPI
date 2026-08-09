from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import DeliveryPartner, Seller
from database.redis import is_jti_blacklisted
from database.session import get_session
from services.delivery_partner import DeliveryPartnerService
from services.seller import SellerService
from services.shipment import ShipmentService
from core.security import oauth2_schema_seller, oauth2_schema_partner
from utils import decode_access_token
from services.shipment import ShipmentService
from services.seller import SellerService

SessionDep = Annotated[AsyncSession, Depends(get_session)]

# Acess token data dependency
# decode the jwt token and extract user information from the token
async def _get_access_token(token: str) -> dict:

    data = decode_access_token(token=token)

    # if the token is invalid or the token id is not in tokens blacklist raise an error
    if data is None or await is_jti_blacklisted(data["user"]["jti"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token"
        )

    return data


async def get_seller_access_token(token: Annotated[str, Depends(oauth2_schema_seller)]) -> dict:
    # Just decode the seller token to extract it's original data
    return await _get_access_token(token=token)

async def get_partner_access_token(token: Annotated[str, Depends(oauth2_schema_partner)]) -> dict:
    # Just decode the delivery partner token to extract it's original data

    return await _get_access_token(token=token)


# Logged In Seller
async def get_current_seller(
    token_data: Annotated[dict, Depends(get_seller_access_token)],
    session: SessionDep
):

    seller = await session.get(Seller, UUID(token_data['user']['id'])) 


    if seller is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized",
        )

    return seller

# Logged In Partner
async def get_current_partner(
    token_data: Annotated[dict, Depends(get_partner_access_token)],
    session: SessionDep
):

    partner = await session.get(DeliveryPartner, UUID(token_data['user']['id'])) 


    if partner is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized"
        )

    return partner

def get_shipment_service(session: SessionDep):
    return ShipmentService(
        session,
        DeliveryPartnerService(session)
    )


def get_seller_service(session: SessionDep):
    return SellerService(session=session)

# Delivery partner service dep
def get_delivery_partner_service(session: SessionDep):
    return DeliveryPartnerService(session=session)

# Seller token dependency
ActiveSellerDep = Annotated[
    Seller,
    Depends(get_current_seller)
]

# Delivery dep
DeliveryPartnerDep = Annotated[
    DeliveryPartner,
    Depends(get_current_partner)
]


# Delivery partner service dep annotation
DeliveryPartnerServiceDep = Annotated[
    DeliveryPartnerService,
    Depends(get_delivery_partner_service)
]

# DeliveryPartnerService
ShipmentServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]
SellerServiceDep = Annotated[SellerService, Depends(get_seller_service)]
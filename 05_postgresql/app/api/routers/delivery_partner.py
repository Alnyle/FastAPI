from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm


from api.dependencies import DeliveryPartnerDep, DeliveryPartnerServiceDep, SellerServiceDep, get_partner_access_token
from api.schemas.delivery_partner import DeliveryPartnerCreate, DeliveryPartnerRead, DeliveryPartnerUpdate
from database.models import Seller
from database.redis import add_jti_to_blaclist
from utils import decode_access_token

router = APIRouter(prefix="/partner", tags=["Delivery Partner"])

# Register a delivery partner
@router.post('/signup', response_model=DeliveryPartnerRead)
async def register_delivery_partner(
    seller: DeliveryPartnerCreate,
    service: DeliveryPartnerServiceDep
):

    return await service.add(seller)


# Login the delivery partner
@router.post("/login")
async def login_delivery_partner(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: DeliveryPartnerServiceDep
):

    # print(f"name: {request_form.username}, password: {request_form.password}")
    token = await service.token(request_form.username, request_form.password)

    return {
        "access_token": token,
        "type": "jwt"
    }


# Upadte the delivery partner 
@router.post('/', response_model=DeliveryPartnerRead)
async def update_delivery_partner(
    partner_update: DeliveryPartnerUpdate,
    partner: DeliveryPartnerDep,
    service: DeliveryPartnerServiceDep,
):
    # Update data with given fields
    update = partner_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided to update",
        )

    return await service.update(
        partner.sqlmodel_update(update),
    )



# Logout the delivery partner
@router.get("/logout")
async def logout_delivery_partner(
    token_data: Annotated[dict, Depends(get_partner_access_token)],
):

    # extract the token id to add it to the blacklist after user logout
    token_id = token_data['jti']

    await add_jti_to_blaclist(token_id)

    return {
        "details": "Successfully logged out"
    }
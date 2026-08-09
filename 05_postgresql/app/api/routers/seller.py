from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm


from api.dependencies import SellerServiceDep, SessionDep, get_seller_access_token
from api.schemas.seller import SellerCreate, SellerRead
from database.models import Seller
from database.redis import add_jti_to_blaclist
from utils import decode_access_token

router = APIRouter(prefix="/seller", tags=["Seller"])


@router.post('/signup', response_model=SellerRead)
async def register_seller(seller: SellerCreate, service: SellerServiceDep):

    return await service.add(seller)


# Login the seller
@router.post("/login")
async def login_seller(request_form: Annotated[OAuth2PasswordRequestForm, Depends()], service: SellerServiceDep):

    # print(f"name: {request_form.username}, password: {request_form.password}")
    token = await service.token(request_form.username, request_form.password)

    return {
        "access_token": token,
        "type": "jwt"
    }


# Logout the seller
@router.get("/logout")
async def logout_seller(
    token_data: Annotated[dict, Depends(get_seller_access_token)],
):

    # extract the token id to add it to the blacklist after user logout
    token_id = token_data['jti']

    await add_jti_to_blaclist(token_id)

    return {
        "details": "Successfully logged out"
    }
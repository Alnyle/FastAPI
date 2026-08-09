from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, HTTPBearer

from utils import decode_access_token


oauth2_schema_seller = OAuth2PasswordBearer(tokenUrl="/seller/login")
oauth2_schema_partner = OAuth2PasswordBearer(tokenUrl="/partner/login")





class AccessTokenBearer(HTTPBearer):

    async def __call__(self, request):

        # Extract the token from thhe request header 
        # token = request.headers.get("Authorization").split(" ")[1]

        # call the parent class (HTTPBearer) call using super constuctor
        # Reads the Authorization header.
        # Checks that it exists.
        # Verifies it uses the Bearer scheme.
        # Extracts the token.
        # Returns an HTTPAuthorizationCredentials object.
        auth_credentials = await super().__call__(request)
        token = auth_credentials.credentials

        token_data = decode_access_token(token)

        if token_data is None:
            raise HTTPException(
                status_code=401,
                detail="Not Authorized"
            )

        return token_data


access_token_bearer = AccessTokenBearer()

oauth2Dep = Annotated[dict, Depends(access_token_bearer)]
import json
import os

import fastapi.security
import jwt
from httpx import AsyncClient
from dotenv import load_dotenv
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPBasicCredentials


load_dotenv()

CLERK_FRONTEND_API = os.getenv("CLERK_FRONTEND_API")
CLERK_API_KEY = os.getenv("CLERK_SECRET_KEY")
CLERK_VERIFY_ENDPOINT = f"https://{CLERK_FRONTEND_API}/v1/tokens/verify"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 30
CLERK_API_SECRET = os.getenv("CLERK_SECRET_KEY")
CLERK_JWKS_URL = os.getenv("CLERK_JWKS_URL")

ALGORITHMS = ["RS256"]

security = HTTPBearer()


async def get_jwks():
    async with AsyncClient() as client:
        response = await client.get(CLERK_JWKS_URL, headers={"Authorization": f"Bearer {CLERK_API_SECRET}"})
        response.raise_for_status()
        return response.json()


async def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    token = credentials.credentials
    jwks = await get_jwks()

    public_key = jwks["keys"][0]
    try:
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            options={"verify_signature": True},
        )
    except jwt.ExpiredSignatureError:
        raise fastapi.exceptions.HTTPException(400, "Token has expired.")
    except jwt.DecodeError:
        raise fastapi.exceptions.HTTPException(401, "Token decode error.")
    except jwt.InvalidTokenError:
        raise fastapi.exceptions.HTTPException(400, "Invalid token.")
    user_id = payload.get("sub")
    return user_id

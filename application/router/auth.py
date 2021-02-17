from fastapi import APIRouter, Depends, Request
from typing import Optional
from pydantic import BaseModel
from config import config
import jwt
import datetime
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter()

@router.get("/auth/jwt/refresh")
async def refreshToken(request: Request):
    try:
        jwtToken = request.headers["www-authenticate"]
        payload = jwt.decode(
            jwtToken,
            config.SECRET_KEY,
            algorithms=[config.ALGORITHM],
            options={"verify_exp": False},
        )
        newJwtToken = jwt.encode({
                **payload, 
                "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=config.ACCESS_TOKEN_EXPIRE_MINUTES*60)
            }, config.SECRET_KEY, algorithm=config.ALGORITHM)
        return {
            "METHOD": "GET",
            "URL": "/auth/jwt/refresh",
            "JWT": newJwtToken
        }
    except Exception as e:
        return {
			"error": {
				"status": True,
				"message": str(e),
				"code": 500
			}
		}


class APILoginData(BaseModel):
    username: str
    browserToken: Optional[str] = None
    password: str
@router.post("/auth/jwt")
async def authentication(inputParam: APILoginData):
    # password verification then doing sending Token
    payload = {
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=config.ACCESS_TOKEN_EXPIRE_MINUTES*60),
        "data": {
            "name": "",
            "username": inputParam.username,
        }
    }
    jwtToken = jwt.encode(payload, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return {
        "METHOD": "POST",
        "URL": "/auth/jwt",
        "JWT": jwtToken
    }
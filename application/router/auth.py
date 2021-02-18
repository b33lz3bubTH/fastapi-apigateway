from fastapi import APIRouter, Depends, Request, HTTPException
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
        jwtToken = request.headers.get("www-authenticate")
        if not jwtToken or len(jwtToken) < 10:
            raise HTTPException(status_code=404, 
                detail="JWT Required",
                headers={"www-authenticate": "bearer"}
            )
        payload = jwt.decode(
            jwtToken,
            config.SECRET_KEY,
            algorithms=[config.ALGORITHM],
            options={"verify_exp": False},
        )
        currentTime = datetime.datetime.utcnow()
        newJwtToken = jwt.encode({
                **payload,
                "iat": currentTime,
                "exp": currentTime + datetime.timedelta(seconds=config.ACCESS_TOKEN_EXPIRE_MINUTES*60)
            }, config.SECRET_KEY, algorithm=config.ALGORITHM)
        return {
            "METHOD": "GET",
            "URL": "/auth/jwt/refresh",
            "JWT": newJwtToken
        }
    except jwt.exceptions.DecodeError as e:
        return HTTPException(status_code=500, 
            detail="JWT Decode Failed",
            headers={"www-authenticate": "bearer"}
            )
    except HTTPException as e:
        return {
            "error": e
        }
    except Exception as e:
        return {
            "error": str(e)
        }

class APILoginData(BaseModel):
    username: str
    browserToken: Optional[str] = None
    password: str
@router.post("/auth/jwt")
async def authentication(inputParam: APILoginData):
    # password verification then doing sending Token
    # {name: "Sourav", password: "HA$HED", email: "xx@gmail.com", phone: "", address: {} }
    currentTime = datetime.datetime.utcnow()
    payload = {
        "exp": currentTime + datetime.timedelta(seconds=config.ACCESS_TOKEN_EXPIRE_MINUTES*60),
        "iat": currentTime,
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
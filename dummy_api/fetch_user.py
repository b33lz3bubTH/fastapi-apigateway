from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()


@app.get("/user/{user_id}")
async def userDataFetch(user_id):
    return {"user": user_id, "msg": "FETCHED SUCCESS FULLY", "code": 200}

@app.get("/admin/{user_id}")
async def userDataFetch(user_id):
    return {"admin": user_id, "msg": "FETCHED SUCCESS FULLY", "code": 200}

class UserInputModel(BaseModel):
    name: str
    description: str
    price: float
    tax: float
@app.post("/user/{user_id}")
async def userDataPost(user_id, inputParam: UserInputModel):
    print(inputParam)
    return {"user": user_id, "msg": "FETCHED SUCCESS FULLY", "code": 200, "data": inputParam}
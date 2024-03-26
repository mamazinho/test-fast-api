import os
from typing import Annotated, Union

import uvicorn
from fastapi import Body, Depends, FastAPI, Header, HTTPException
from fastapi.security.utils import get_authorization_scheme_param
from jose import jwt
from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float | None = None


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/queryparams/")
def read_item_q(**q):
    return {"q": q}


def get_current_user():
    return User(
        username="math", email="math@gmail.com", full_name="matheus", disabled=False
    )


@app.get("/me/")
def get_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@app.post("/user/{user_id}")
def create_user(
    current_user: Annotated[User, Depends(get_current_user)],
    user_id: str,
    item: Item,
    importance: Annotated[int, Body()],
    q: str | None = None,
):
    return {
        "current_user": current_user,
        "user_id": user_id,
        "item": item,
        "importance": importance,
        "q": q,
    }


def get_auth_current_user(authorization: Annotated[str | None, Header()]):
    _, token = get_authorization_scheme_param(authorization)
    res = jwt.decode(token, "secret", algorithms=["HS256"])

    machine_id = res.get("machine_id")

    if not machine_id:
        raise HTTPException(status_code=401, detail="user has no access")
    return machine_id


@app.get("/authme/", dependencies=[Depends(get_auth_current_user)])
def get_me_auth(
    x_api_key: Annotated[str, Header()],
):  # , current_user: Annotated[str, Depends(get_auth_current_user)]):
    return {
        "api_key": x_api_key,
        # "current_user": current_user,
    }


if __name__ == "__main__":
    app_name = os.path.basename(__file__).replace(".py", "")
    uvicorn.run(
        app=f"{app_name}:app", host="0.0.0.0", port=8080, workers=1, reload=True
    )

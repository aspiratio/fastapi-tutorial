from fastapi import FastAPI
from enum import Enum


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()  # FastAPIのインスタンス化


@app.get("/")  # インスタンス化したappにHTTPメソッド（オペレーションと呼ぶ）のGETで"/"のURLにアクセスがあったら下の関数を実行するという意味
async def root():
    return {"message": "Hello World"}


@app.get("/user/{id}")
async def get_user_id(id: int):
    return {"user_id": id, "user_name": f"user_{id}"}


@app.get("/user_list")
async def get_user_list():
    return {"users": ["Taro", "Jiro", "Saburo"]}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    # model_name には ModelName.alexnet, ModelName.lenet, ModelName.resnet のいずれかが入る
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

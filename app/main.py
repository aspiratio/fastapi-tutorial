from fastapi import FastAPI
from enum import Enum
from typing import Optional, Union


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()  # FastAPIのインスタンス化


# 基本
@app.get("/")  # インスタンス化したappにHTTPメソッド（オペレーションと呼ぶ）のGETで"/"のURLにアクセスがあったら下の関数を実行するという意味
async def root():
    return {"message": "Hello World"}


# パスパラメータ
@app.get("/user/{id}")
async def get_user_id(id: int):
    return {"user_id": id, "user_name": f"user_{id}"}


# JSONの中にリスト
@app.get("/user_list")
async def get_user_list():
    return {"users": ["Taro", "Jiro", "Saburo"]}


# Enum
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    # model_name には ModelName.alexnet, ModelName.lenet, ModelName.resnet のいずれかが入る
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


# パス変換
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


# クエリパラメータ
@app.get("/countries/")  # パスパラメータを設定しなければクエリパラメータとみなされる
async def get_countries(
    country_name: str = "America", city_name: str = "NewYork"
):  # デフォルトの値を設定可能
    return {"country_name": country_name, "city_name": city_name}


# パスパラメータ＋クエリパラメータ
@app.get("/countries/{country_name}")
async def get_countries(
    country_name: str = "America", city_name: str = "NewYork"
):  # パスパラメータに指定したやつ以外をクエリパラメータとして自動で識別してくれる
    return {"country_name": country_name, "city_name": city_name}


# オプショナルパラメータ
@app.get("/items/")
async def get_items(
    q: Optional[str] = "test",  # Optionalを使うと str | None つまり任意のパラメータになる
):
    return {"q": q}


# 複数の型指定
@app.get("/items/{item_id}")
async def get_item(
    item_id: Union[int, float],  # 複数の型指定ができる
    q: Union[str, None] = "test",  # Optional[str] と同じ使い方ができる
):
    return {"item_id": item_id, "q": q}

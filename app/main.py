from fastapi import FastAPI, Query, Path, Body
from enum import Enum
from typing import Optional, Union, List, Annotated
from pydantic import BaseModel


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()  # FastAPIのインスタンス化


# 基本（GET）
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
):  # デフォルトの値を設定可能（任意のパラメータにできる）
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
    q: Optional[str] = None,  # Optionalを使うと str | None つまりデフォルト値をNoneにできる
):
    return {"q": q}


# 複数の型指定
@app.get("/items/{item_id}")
async def get_item(
    item_id: Union[int, float],  # 複数の型指定ができる
    q: Union[str, None] = None,  # Optional[str] と同じ使い方ができる
):
    return {"item_id": item_id, "q": q}


# bool型の使用
@app.get("/answer/{boolean}")
async def get_answer_path(boolean: bool):
    # True, 1, on, yes は true として扱われる
    # False, 0, off, no は false として扱われる
    return {"boolean": boolean}


# 複数のパラメータ
@app.get("/users/{user_id}/items/{item_id}")
async def get_user_item(item_id: int, user_id: str):  # 引数は順不同
    return {"user_id": user_id, "item_id": item_id}


# クエリパラメータにバリデーションを設定
@app.get("/products/")
async def read_products(
    q: Union[str, None] = Query(
        default=None, min_length=3, max_length=50, pattern="^fixedquery$"
    )
):  # ここではデフォルト値の設定と文字数の制限を行なっている
    results = {"products": [{"product_id": "Foo"}, {"product_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 同じクエリパラメータで複数の値を受け取る ex: http://localhost:8000/items/?q=foo&q=bar
@app.get("/contents/")
async def read_contents(
    q: List[str] = Query(default=["foo", "bar"], min_length=3, max_length=50)
):  # 文字数制限は各値（fooやbar）に適応される
    query_items = {"q": q}
    return query_items


# クエリパラメータにメタデータを設定する
@app.get("/items/v2/")
async def get_items_v2(
    q: Union[str, None] = Query(
        default=None,
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# エイリアスパラメータ（クエリパラメータが命名規則にそぐわない場合などに使う）
@app.get("/items/v3/")
async def get_items_v3(q: Union[str, None] = Query(default=None, alias="item-query")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 非推奨パラメータであることを明記（ドキュメントに反映される）
@app.get("/items/v4/")
async def get_items_v4(
    q: Union[str, None] = Query(default=None, alias="item-query", deprecated=True)
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Annotated でメタデータやバリデーションの追加 pythonやFastAPIのバージョンに注意
@app.get("/items/v5/{item_id}")
async def get_items_v5(
    item_id: Annotated[
        int, Path(title="The ID of the item to get", ge=1)
    ],  # ge1は1以上の意味
    q: Annotated[Union[str, None], Query(alias="item-query")] = None,
):
    results = {"items": item_id}
    if q:
        results.update({"q": q})
    return results


# データモデルの作成
class Item(BaseModel):
    name: str
    description: Union[str, None] = None  # Noneに限らず、何かしらのデフォルト値を持たせると任意の属性になる
    price: float
    tax: Union[float, None] = None


class User(BaseModel):
    nickname: str
    full_name: Union[str, None] = None


# POST
@app.post("/items/")
async def add_price_with_tax(item: Item):
    # BaseModel.property で各要素にアクセスできる
    if item.tax:
        price_with_tax = item.price * item.tax
    else:
        item.description = "消費税なし"
        price_with_tax = item.price
    item_dict = item.dict()
    item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


# ボディとパスパラメータを併用
@app.post("/items/{item_id}")
async def create_item(item_id: int, item: Item):  # パスパラメータ以外は自動でリクエストボディから受け取る
    return {"item_id": item_id, **item.dict()}


# ボディとパスパラメータとクエリパラメータを併用
@app.post("/items/v2/{item_id}")
async def create_item_v2(
    item_id: int,
    item: Item,
    q: Union[str, None] = None,
):  # データ型が単数型なら、Bodyではなくクエリパラメータとして認識する
    """
    リクエストボディの例
    {
      "name": "string",
      "description": "string",
      "price": 0,
      "tax": 0
    }
    """
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result


# 複数のボディパラメータを使用
@app.post("/items/v3/{item_id}")
async def update_item_v3(item_id: int, item: Item, user: User):
    """
    リクエストボディの例
    {
      "item": {
        "name": "pen",
        "description": "for writing",
        "price": 100,
        "tax": 10
      },
      "user": {
        "nickname": "Taro",
        "full_name": "Taro Aso"
      }
    }
    """
    results = {"item_id": item_id, "item": item, "user": user}
    return results


# PUT
# データモデルを使わずにボディパラメータを宣言する
@app.put("/items/v4/{item_id}")
async def update_item_v4(
    item_id: int,
    item: Item,
    user: User,
    importance: Annotated[
        Union[int, None], Body(gt=0)
    ] = 0,  # ボディに任意のパラメータ（0以上の数値）があるという意味になる
):
    """
    {
      "item": {
        "name": "string",
        "description": "string",
        "price": 0,
        "tax": 0
      },
      "user": {
        "nickname": "string",
        "full_name": "string"
      },
      "importance": 10
    }
    """
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results

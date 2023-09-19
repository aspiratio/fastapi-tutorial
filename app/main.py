from fastapi import FastAPI

app = FastAPI()  # FastAPIのインスタンス化


@app.get("/")  # インスタンス化したappにHTTPメソッド（オペレーションと呼ぶ）のGETで"/"のURLにアクセスがあったら下の関数を実行するという意味
async def root():
    return {"message": "Hello World"}


@app.get(
    "/user/{id}"
)  # インスタンス化したappにHTTPメソッド（オペレーションと呼ぶ）のGETで"/"のURLにアクセスがあったら下の関数を実行するという意味
async def get_user_id(id: int):
    return {"item_id": id}

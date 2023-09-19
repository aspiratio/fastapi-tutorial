# 実行したコマンド

## Docker イメージの作成

```sh
docker build --platform linux/arm64/v8 -t fastapi-tutorial .
```

- `--platform`: `linux/amd64/v8` を指定することで M1 チップのマックでコンテナを作れるようにする
- `-t`: ビルドするイメージの名前をつける

## コンテナの作成

### Docker Compose を使用しない場合

この方法だと、毎回コンテナを手動で削除する必要がある

```sh
docker run -it -v ${pwd}/app:/app -p 8080:8000  --name fastapi_container fastapi-tutorial /bin/bash
```

- `-it`: コンテナ作成と同時に、コンテナ内のターミナルに接続できる
- `-v`: ホストとコンテナ内のディレクトリの中身を同期する（`${pwd}`は任意のパスに書き換える）
- `-p`: ホストのポートとコンテナ内のポートをリンクする
- `--name`: コンテナに名前をつける
- `/bin/bash`: コンテナ内で/bin/bash シェルを実行する

### Docker Compose を使用する場合

コンテナの起動時に自動で前回のコンテナを停止・削除してくれる

```sh
docker exec -it fastapi_container /bin/bash
```

- `-it`: コンテナ内のターミナルに接続できる

## ライブサーバーの実行（以下のコマンドはコンテナ内のシェルで実行する）

```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

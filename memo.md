# 実行したコマンド

## Docker イメージの作成

```sh
docker build --platform linux/arm64/v8 -t fastapi-tutorial .
```

### 解説

- `--platform`: `linux/amd64/v8` を指定することで M1 チップのマックでコンテナを作れるようにする
- `-t`: ビルドするイメージの名前をつける

## Docker コンテナの作成

```sh
docker run -it -v ${pwd}/app:/app -p 8080:8000  --name fastapi_container fastapi-tutorial /bin/bash
```

### 解説

- `-it`: コンテナ作成と同時に、コンテナ内のターミナルに接続できる
- `-v`: ホストとコンテナ内のディレクトリの中身を同期する（`${pwd}`は任意のパスに書き換える）
- `-p`: ホストのポートとコンテナ内のポートをリンクする
- `--name`: コンテナに名前をつける
- `/bin/bash`: コンテナ内で/bin/bash シェルを実行する

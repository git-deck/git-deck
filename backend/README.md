## OAuthの設定

1. https://github.com/settings/applications/new でOAuthアプリケーションを登録.
Authorization callback URLは http://localhost:3000/callback に設定すること.

2. .env を作る.

```
GITHUB_CLIENT_ID={1.で作成したClient ID}
GITHUB_CLIENT_SECRET={1.で作成したClient secrets}
```

## データベースの設定

1. flaskコンテナとdbコンテナを起動する.
```
docker compose up flask db
```

2. flaskコンテナに接続し, データベースのmigrationを行う.
```
docker exec -it issue-backend /bin/bash
flask db init
flask db migrate
flask db upgrade
```

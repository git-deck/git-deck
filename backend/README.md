## OAuthの確認方法

1. https://github.com/settings/applications/new でOAuthアプリケーションを登録.
Authorization callback URLは http://localhost:5000/callback/github に設定すること.

2. backend/.env を作る.

```
GITHUB_CLIENT_ID={1.で作成したClient ID}
GITHUB_CLIENT_SECRET={1.で作成したClient secrets}
FLASK_SECRET_KEY={適当な値}
```

4. dockerコンテナを起動
```
docker compose up
```

5. http://localhost:5000/oauth にアクセスし, 飛ばされたページでAuthorizeする

6. http://localhost:5000/user にリダイレクトされて, Githubのユーザ名が表示されてたらOK

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
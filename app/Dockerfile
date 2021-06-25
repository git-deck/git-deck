# イメージ指定
FROM node:12.13.0-alpine

# m1対応
RUN apk update && \
    apk add --no-cache python make g++

# locale & timezone (Asia/Tokyo)
ENV LANG C.UTF-8
ENV TZ Asia/Tokyo

# コマンド実行
RUN npm uninstall -g yarn && \
    npm install -g yarn && \
    yarn install && \
    yarn global add @vue/cli nuxt create-nuxt-app

# コンテナソースパス作成・移動
WORKDIR /app/front
# パッケージインストール
RUN yarn
# Port公開
EXPOSE 3000
# 開発サーバー立ち上げ(installの差分がある場合実行に時間がかかる)
CMD sh -c "cd app/front && yarn install && yarn run dev"

ENV CHOKIDAR_USEPOLLING=true
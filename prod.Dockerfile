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
COPY webapp /home
WORKDIR /home

# パッケージインストール
RUN yarn

# productionモードで立ち上げ
ARG GITHUB_CLIENT_ID
ARG GITHUB_CLIENT_SECRET
ENV NUXT_ENV_GITHUB_CLIENT_ID=$GITHUB_CLIENT_ID
ENV NUXT_ENV_GITHUB_CLIENT_SECRET=$GITHUB_CLIENT_SECRET
ENV HOST=0.0.0.0
RUN yarn build
CMD sh -c "yarn run start"

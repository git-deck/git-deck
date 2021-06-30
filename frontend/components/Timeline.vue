<template>
  <div class="column">
    <header>
      <span> <Octicon :icon="Octicons.repo" class-name="repoicon" /> </span>
      <span class="title"
        ><a class="username" href="https://github.com/knknk98/">knknk98/</a
        ><a class="reponame" href="https://github.com/knknk98/sushi-chat/"
          >sushi-sushi-sushi</a
        ></span
      >
      <button class="chat" @click="showModal">
        <span class="material-icons"> chat_bubble_outline </span>
      </button>
      <button class="tune" @click="clickSettings">
        <span class="material-icons"> tune </span>
      </button>
    </header>
    <modal name="editor-modal">投稿画面</modal>
    <Setting v-if="settingOpened" />
    <main>
      <Content v-for="(content,index) in contents" :key="index" type="idea"></Content>
      <Comment type="pullRequest" thread />
      <Comment type="reply" thread />
      <Comment type="reply" thread />
      <Comment type="reply" />
      <Comment type="issue" />
      <Comment type="idea" />
    </main>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { Content, Idea } from '@/models/types'

const { Octicon, Octicons } = require('octicons-vue')

type DataType = {
  Octicons: any
  settingOpened: boolean
  contents: Content[]
}

export default Vue.extend({
  components: { Octicon },
  data(): DataType {
    return {
      Octicons,
      settingOpened: false,
      contents: CONTENTS_DUMMY_DATA
    }
  },
  methods: {
    // ラベル絞り込みボタンの開閉
    clickSettings() {
      this.settingOpened = !this.settingOpened
    },
    showModal() {
      this.$modal.show('editor-modal')
    },
  },
})

// FIXME: テストデータを入れたいけど, Cannot set property 'category' of undefined と怒られる.
// FIXME: テストデータを入れたいけど, Cannot set property 'category' of undefined と怒られる.
// FIXME: テストデータを入れたいけど, Cannot set property 'category' of undefined と怒られる.
const CONTENTS_DUMMY_DATA: Content[] = [
    //{
    //    author: {
    //        avatarUrl: "https://avatars.githubusercontent.com/u/34413567?v=4",
    //        login: "habara-k",
    //        url: "https://github.com/habara-k"
    //    },
    //    body: "あぁ^～心がぴょんぴょんするんじゃぁ^～",
    //    category: "idea",
    //    howLongAgo: "1h",
    //},
    // {
    //     assignees: [
    //         {
    //             avatarUrl: "https://avatars.githubusercontent.com/u/34413567?v=4",
    //             login: "habara-k",
    //             url: "https://github.com/habara-k"
    //         }
    //     ],
    //     author: {
    //         avatarUrl: "https://avatars.githubusercontent.com/u/34413567?v=4",
    //         login: "habara-k",
    //         url: "https://github.com/habara-k"
    //     },
    //     body: "",
    //     category: "pullRequest",
    //     comments: [],
    //     howLongAgo: "16h",
    //     labels: [
    //         {
    //             color: "d73a4a",
    //             name: "bug"
    //         }
    //     ],
    //     number: 21,
    //     state: "MERGED",
    //     title: "[Fix] GET /timeline",
    //     url: "https://github.com/knknk98/issue-twitter/pull/21"
    // },
    // {
    //     assignees: [
    //         {
    //             avatarUrl: "https://avatars.githubusercontent.com/u/34413567?v=4",
    //             login: "habara-k",
    //             url: "https://github.com/habara-k"
    //         }
    //     ],
    //     author: {
    //         avatarUrl: "https://avatars.githubusercontent.com/u/34413567?v=4",
    //         login: "habara-k",
    //         url: "https://github.com/habara-k"
    //     },
    //     body: "## 問題点\r\n\r\ndbコンテナの`mysqld`が立ち上がる前に、flaskコンテナのアプリがdbに接続しに行っちゃう。\r\n\r\nそのため、時間を空けて別々に立ち上げないとバグる。\r\n\r\nhttps://github.com/knknk98/issue-twitter/pull/10#issue-678574393",
    //     category: "issue",
    //     comments: [
    //         {
    //             author: {
    //                 avatarUrl: "https://avatars.githubusercontent.com/u/34413567?v=4",
    //                 login: "habara-k",
    //                 url: "https://github.com/habara-k"
    //             },
    //             body: "https://github.com/knknk98/issue-twitter/pull/13",
    //             howLongAgo: "2d",
    //             url: "https://github.com/knknk98/issue-twitter/issues/11#issuecomment-869223795"
    //         }
    //     ],
    //     howLongAgo: "2d",
    //     labels: [
    //         {
    //             color: "d73a4a",
    //             name: "bug"
    //         },
    //         {
    //             color: "008672",
    //             name: "help wanted"
    //         }
    //     ],
    //     number: 11,
    //     state: "CLOSED",
    //     title: "現状flaskとdbを別々に立ち上げる必要がある",
    //     url: "https://github.com/knknk98/issue-twitter/issues/11"
    // },
    // {
    //     assignees: [
    //         {
    //             avatarUrl: "https://avatars.githubusercontent.com/u/34413567?v=4",
    //             login: "habara-k",
    //             url: "https://github.com/habara-k"
    //         }
    //     ],
    //     author: {
    //         avatarUrl: "https://avatars.githubusercontent.com/u/34413567?v=4",
    //         login: "habara-k",
    //         url: "https://github.com/habara-k"
    //     },
    //     body: "https://github.com/knknk98/issue-twitter/issues/11\r\n\r\n参考: https://stackoverflow.com/questions/42567475/docker-compose-check-if-mysql-connection-is-ready",
    //     category: "pullRequest",
    //     comments: [],
    //     howLongAgo: "2d",
    //     labels: [
    //         {
    //             color: "d73a4a",
    //             name: "bug"
    //         }
    //     ],
    //     number: 13,
    //     state: "MERGED",
    //     title: "Fix: mysqldが立ち上がるまでflaskを待機させる",
    //     url: "https://github.com/knknk98/issue-twitter/pull/13"
    // },
    // {
    //     assignees: [
    //         {
    //             avatarUrl: "https://avatars.githubusercontent.com/u/34413567?v=4",
    //             login: "habara-k",
    //             url: "https://github.com/habara-k"
    //         }
    //     ],
    //     author: {
    //         avatarUrl: "https://avatars.githubusercontent.com/u/34413567?v=4",
    //         login: "habara-k",
    //         url: "https://github.com/habara-k"
    //     },
    //     body: "",
    //     category: "pullRequest",
    //     comments: [],
    //     howLongAgo: "2d",
    //     labels: [
    //         {
    //             color: "d73a4a",
    //             name: "bug"
    //         }
    //     ],
    //     number: 9,
    //     state: "MERGED",
    //     title: "Fix requirements.txt",
    //     url: "https://github.com/knknk98/issue-twitter/pull/9"
    // }
]
</script>

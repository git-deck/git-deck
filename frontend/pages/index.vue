<template>
  <div class="container">
    <Sidebar @appendTimeline="append" />
    <Timeline
      v-for="(tl, index) in timeline"
      :key="index"
      :owner="tl.owner"
      :repo="tl.repo"
      :owner-url="tl.ownerUrl"
      :repo-url="tl.repoUrl"
      :contents="tl.contents"
    />
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import VModal from 'vue-js-modal'
import { Content } from '@/models/types'
import axios from 'axios'

axios.defaults.baseURL = 'http://localhost:5000'

Vue.use(VModal)

type DataType = {
  timeline: Object[]
}
export default Vue.extend({
  data(): DataType {
    return {
      timeline: [
        {
          owner: 'knknk98',
          repo: 'issue-twitter',
          ownerUrl: 'https://github.com/knknk98',
          repoUrl: 'https://github.com/knknk98/issue-twitter',
          contents: CONTENTS_DUMMY_DATA,
        },
      ],
    }
  },
  methods: {
    append(owner: string, repo: string) {
      const self = this
      axios
        .get('/timeline/' + owner + '/' + repo, {
          headers: {
            Authorization: this.$auth.getToken('github'),
          },
        })
        .then(function (response) {
          console.log(response)
          self.timeline.push({
            owner,
            repo,
            ownerUrl: 'https://github.com/' + owner,
            repoUrl: 'https://github.com/' + owner + '/' + repo,
            contents: response.data,
          })
        })
        .catch(function (error) {
          console.log(error)
        })
        .then(function () {
          // always executed
        })
    },
  },
})

const CONTENTS_DUMMY_DATA: Content[] = [
  {
    assignees: [
      {
        avatarUrl: 'https://avatars.githubusercontent.com/u/34413567?v=4',
        login: 'habara-k',
        url: 'https://github.com/habara-k',
      },
    ],
    author: {
      avatarUrl: 'https://avatars.githubusercontent.com/u/34413567?v=4',
      login: 'habara-k',
      url: 'https://github.com/habara-k',
    },
    body: '',
    category: 'pullRequest',
    comments: [
      {
        author: {
          avatarUrl: 'https://avatars.githubusercontent.com/u/34413567?v=4',
          login: 'habara-k',
          url: 'https://github.com/habara-k',
        },
        body: 'HELP!! \r\nhttps://github.com/knknk98/issue-twitter/blob/b0aa3068041d6ffd8d1c351b7567dbb44f9108d5/frontend/components/Timeline.vue#L64-L66',
        howLongAgo: '23h',
        url: 'https://github.com/knknk98/issue-twitter/pull/26#issuecomment-871321394',
      },
      {
        author: {
          avatarUrl: 'https://avatars.githubusercontent.com/u/34413567?v=4',
          login: 'habara-k',
          url: 'https://github.com/habara-k',
        },
        body: '<img width="458" alt="スクリーンショット 2021-06-30 23 36 16" src="https://user-images.githubusercontent.com/34413567/123981299-325f6d00-d9fd-11eb-91fa-f2b513f0507f.png">\r\n',
        howLongAgo: '19h',
        url: 'https://github.com/knknk98/issue-twitter/pull/26#issuecomment-871468660',
      },
      {
        author: {
          avatarUrl: 'https://avatars.githubusercontent.com/u/38308823?v=4',
          login: 'yuta-ike',
          url: 'https://github.com/yuta-ike',
        },
        body: 'やったぁ🎉🎉',
        howLongAgo: '19h',
        url: 'https://github.com/knknk98/issue-twitter/pull/26#issuecomment-871472214',
      },
      {
        author: {
          avatarUrl:
            'https://avatars.githubusercontent.com/u/65712721?u=8d33b92b7c5cca2cdfaa755054a865131d8704c7&v=4',
          login: 'knknk98',
          url: 'https://github.com/knknk98',
        },
        body: '![LGTM](https://image.lgtmoon.dev/132319)',
        howLongAgo: '19h',
        url: 'https://github.com/knknk98/issue-twitter/pull/26#issuecomment-871472788',
      },
    ],
    howLongAgo: '19h',
    labels: [
      {
        color: '#008672',
        name: 'help wanted',
      },
    ],
    number: 26,
    state: 'MERGED',
    title: 'TLにAPIを繋げる',
    url: 'https://github.com/knknk98/issue-twitter/pull/26',
  },
  {
    author: {
      avatarUrl: 'https://github.com/habara-k.png',
      login: 'habara-k',
      url: 'https://github.com/habara-k',
    },
    body: 'あぁ^～心がぴょんぴょんするんじゃぁ^～',
    category: 'idea',
    howLongAgo: '1h',
  },
  {
    assignees: [
      {
        avatarUrl: 'https://github.com/habara-k.png',
        login: 'habara-k',
        url: 'https://github.com/habara-k',
      },
    ],
    author: {
      avatarUrl: 'https://github.com/habara-k.png',
      login: 'habara-k',
      url: 'https://github.com/habara-k',
    },
    body: '',
    category: 'pullRequest',
    comments: [],
    howLongAgo: '16h',
    labels: [
      {
        color: '#8EF61B',
        name: 'speed up',
      },
    ],
    number: 21,
    state: 'OPEN',
    title: '[Fix] GET /timeline',
    url: 'https://github.com/knknk98/issue-twitter/pull/21',
  },
  {
    assignees: [
      {
        avatarUrl: 'https://github.com/habara-k.png',
        login: 'habara-k',
        url: 'https://github.com/habara-k',
      },
    ],
    author: {
      avatarUrl: 'https://github.com/habara-k.png',
      login: 'habara-k',
      url: 'https://github.com/habara-k',
    },
    body: '## 問題点\r\n\r\ndbコンテナの`mysqld`が立ち上がる前に、flaskコンテナのアプリがdbに接続しに行っちゃう。\r\n\r\nそのため、時間を空けて別々に立ち上げないとバグる。\r\n\r\nhttps://github.com/knknk98/issue-twitter/pull/10#issue-678574393',
    category: 'issue',
    comments: [
      {
        author: {
          avatarUrl: 'https://github.com/habara-k.png',
          login: 'habara-k',
          url: 'https://github.com/habara-k',
        },
        body: 'https://github.com/knknk98/issue-twitter/pull/13',
        howLongAgo: '2d',
        url: 'https://github.com/knknk98/issue-twitter/issues/11#issuecomment-869223795',
      },
    ],
    howLongAgo: '2d',
    labels: [
      {
        color: '#d73a4a',
        name: 'bug',
      },
      {
        color: '#008672',
        name: 'help wanted',
      },
    ],
    number: 11,
    state: 'CLOSED',
    title: '現状flaskとdbを別々に立ち上げる必要がある',
    url: 'https://github.com/knknk98/issue-twitter/issues/11',
  },
  {
    assignees: [
      {
        avatarUrl: 'https://github.com/habara-k.png',
        login: 'habara-k',
        url: 'https://github.com/habara-k',
      },
      {
        avatarUrl: 'https://github.com/knknk98.png',
        login: 'knknk98',
        url: 'https://github.com/knknk98',
      },
      {
        avatarUrl: 'https://github.com/knknk98.png',
        login: 'knknk98',
        url: 'https://github.com/knknk98',
      },
      {
        avatarUrl: 'https://github.com/knknk98.png',
        login: 'knknk98',
        url: 'https://github.com/knknk98',
      },
    ],
    author: {
      avatarUrl: 'https://github.com/habara-k.png',
      login: 'habara-k',
      url: 'https://github.com/habara-k',
    },
    body: 'https://github.com/knknk98/issue-twitter/issues/11\r\n\r\n参考: https://stackoverflow.com/questions/42567475/docker-compose-check-if-mysql-connection-is-ready',
    category: 'pullRequest',
    comments: [],
    howLongAgo: '2d',
    labels: [
      {
        color: '#d73a4a',
        name: 'bug',
      },
    ],
    number: 13,
    state: 'MERGED',
    title: 'Fix: mysqldが立ち上がるまでflaskを待機させる',
    url: 'https://github.com/knknk98/issue-twitter/pull/13',
  },
  {
    assignees: [
      {
        avatarUrl: 'https://github.com/habara-k.png',
        login: 'habara-k',
        url: 'https://github.com/habara-k',
      },
      {
        avatarUrl: 'https://github.com/knknk98.png',
        login: 'knknk98',
        url: 'https://github.com/knknk98',
      },
    ],
    author: {
      avatarUrl: 'https://github.com/knknk98.png',
      login: 'knknk98',
      url: 'https://github.com/knknk98',
    },
    body: '',
    category: 'pullRequest',
    comments: [],
    howLongAgo: '2d',
    labels: [
      {
        color: '#0075ca',
        name: 'documentation',
      },
    ],
    number: 9,
    state: 'MERGED',
    title: 'Fix requirements.txt',
    url: 'https://github.com/knknk98/issue-twitter/pull/9',
  },
]
</script>

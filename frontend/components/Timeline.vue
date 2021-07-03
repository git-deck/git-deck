<template>
  <div class="column pane">
    <header>
      <span> <Octicon :icon="Octicons.repo" class-name="repoicon" /> </span>
      <span class="title">
        <a class="username" :href="ownerUrl" target="_blank">{{ owner }}</a>
        /
        <a class="reponame" :href="repoUrl" target="_blank">{{ repo }}</a>
      </span>
      <button class="chat" @click="showModal">
        <span class="material-icons"> add </span>
      </button>
      <button class="Refresh" @click="search">
        <span class="material-icons"> replay </span>
      </button>
      <button class="tune" @click="clickSettings">
        <span class="material-icons"> tune </span>
      </button>
    </header>
    <Setting
      v-show="settingOpened"
      ref="setting"
      :labelItems="labelItems"
      :allLabel="allLabel"
      :categoryLabels="categoryLabels"
      @loadTimeline="search"
      @closeTimeline="close"
      @clickLabel="clickLabel"
    />
    <main>
      <div v-if="isLoading" class="loading">
        <img src="@/assets/img/loading.gif" />
      </div>
      <ContentBox
        v-for="(content, index) in contents"
        :key="index"
        :content="content"
      ></ContentBox>
    </main>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { Content, Label } from '@/models/types'
import axios from 'axios'
// @ts-ignore
import { Octicon, Octicons } from 'octicons-vue'

axios.defaults.baseURL = 'http://localhost:5000'


type LabelItem = {
  label: Label
  labelOpened: Boolean
}

type DataType = {
  Octicons: any
  settingOpened: boolean
  contents: Content[]
  labelItems: LabelItem[]
  isLoading: boolean
  // setting から持ってきた
  categoryLabels: Array<LabelItem>
  allLabel: Label
}

export default Vue.extend({
  components: { Octicon },

  props: {
    id: {
      type: Number,
      required: true,
    },
    useDummyData: {
      type: Boolean,
      default: false,
    },
    owner: {
      type: String,
      required: true,
    },
    repo: {
      type: String,
      required: true,
    },
  },

  data(): DataType {
    return {
      Octicons,
      settingOpened: false,
      contents: [],
      labelItems: [],
      isLoading: false,
      allLabel: JSON.parse(JSON.stringify(ALL_LABEL)), // copy
      categoryLabels: JSON.parse(JSON.stringify(CATEGORY_LABELS)), // copy
    }
  },

  computed: {
    ownerUrl() {
      return 'https://github.com/' + this.owner
    },
    repoUrl() {
      return 'https://github.com/' + this.owner + '/' + this.repo
    },
  },

  created() {
    this.load()
  },

  methods: {
    close() {
      this.$emit('closeTimeline', this.id)
    },
    search() {
      // ダミーデータは検索しない
      if (this.useDummyData) {
        this.contents = CONTENTS_DUMMY_DATA
        this.labelItems = LABELS_DUMMY_DATA.map((label) => ({
          label,
          labelOpened: true,
        }))
        return
      }

      // Build URL

      let url = '/timeline/' + this.owner + '/' + this.repo + '?'
      if (this.allLabel.labelOpened) {
        // すべてラベルがついてなかったら
        const labels = []
        for (const i in this.labelItems) {
          if (!this.labelItems[i].labelOpened) {
            labels.push(this.labelItems[i].label.name)
          }
        }
        if (labels.length > 0) {
          url += 'labels=' + labels.join() + '&'
        }
      }

      const categories = []
      for (const i in this.categoryLabels) {
        if (!this.categoryLabels[i].labelOpened) {
          categories.push(this.categoryLabels[i].label.name)
        }
      }
      if (categories.length > 0) {
        url += 'categories=' + categories.join()
      }
      console.log(url)


      // Send Request
      const self = this
      this.isLoading = true
      axios
        .get(url, {
          headers: {
            Authorization: this.$auth.getToken('github'),
          },
        })
        .then((response) => {
          console.log('response.data:', response.data)
          self.contents = response.data
          this.isLoading = false
        })
        .catch((errors) => {
          // react on errors.
          console.error(errors)
        })
    },

    // ロード時はフィルタなし
    load() {
      console.log('useDummyData:', this.useDummyData)
      if (this.useDummyData) {
        this.contents = CONTENTS_DUMMY_DATA
        this.labelItems = LABELS_DUMMY_DATA.map((label) => ({
          label,
          labelOpened: true,
        }))
        return
      }

      // Send Request
      const timelineRequest = axios.get(
        '/timeline/' +
          this.owner +
          '/' +
          this.repo +
          '?categories=idea,open,closed,merged',
        {
          headers: {
            Authorization: this.$auth.getToken('github'),
          },
        }
      )
      const labelsRequest = axios.get(
        '/labels/' + this.owner + '/' + this.repo,
        {
          headers: {
            Authorization: this.$auth.getToken('github'),
          },
        }
      )
      const self = this
      this.isLoading = true
      axios
        .all([timelineRequest, labelsRequest])
        .then(
          axios.spread((...responses) => {
            self.contents = responses[0].data
            self.labelItems = []
            self.labelItems = responses[1].data.map((label) => ({
              label,
              labelOpened: true,
            }))
            this.isLoading = false
          })
        )
        .catch((errors) => {
          // react on errors.
          console.error(errors)
        })
    },
    // ラベル絞り込みボタンの開閉
    clickSettings() {
      this.settingOpened = !this.settingOpened
    },
    showModal() {
      this.$emit('openPostModal', this.owner, this.repo)
    },

    // ラベルのON OFF管理
    clickLabel(Blockname: string, index: number) {
      // labelOpened:false->選択中
      if (Blockname === 'category') {
        this.categoryLabels[index].labelOpened =
          !this.categoryLabels[index].labelOpened
      }
      if (Blockname === 'labels') {
        if (index === -1) {
          if (this.allLabel.labelOpened) {
            // すべて：選択中でないときにボタン押した
            this.labelItems.map((element) => (element.labelOpened = true))
            this.allLabel.labelOpened = false
          } else {
            this.allLabel.labelOpened = !this.allLabel.labelOpened
          }
        } else if (!this.allLabel.labelOpened) {
          this.allLabel.labelOpened = !this.allLabel.labelOpened
          this.labelItems[index].labelOpened =
            !this.labelItems[index].labelOpened
        } else {
          this.labelItems[index].labelOpened =
            !this.labelItems[index].labelOpened
        }
      }
    },
  },
})

const ALL_LABEL: LabelItem = {
  label: {
    name: 'すべて',
    color: '#24292E',
  },
  labelOpened: false,
}

const CATEGORY_LABELS: LabelItem[] = [
  {
    label: {
      color: '#FFB800',
      name: 'idea',
    },
    labelOpened: false,
  },
  {
    label: {
      color: '#2EA44F',
      name: 'open',
    },
    labelOpened: false,
  },
  {
    label: {
      color: '#bd2c00',
      name: 'closed',
    },
    labelOpened: false,
  },
  {
    label: {
      color: '#6e5494',
      name: 'merged',
    },
    labelOpened: false,
  },
]

const LABELS_DUMMY_DATA: Label[] = [
  {
    color: '#ff0f00',
    name: 'label',
  },
  {
    color: '#00ffff',
    name: 'bug',
  },
  {
    color: '#0000ff',
    name: 'bug',
  },
  {
    color: '#00ff00',
    name: 'bug',
  },
  {
    color: '#00f0f0',
    name: 'bug',
  },
  {
    color: '#0000ff',
    name: 'bug',
  },
  {
    color: '#00ff00',
    name: 'ggggggggggggggggggggggggggggggggggggggggggg',
  },
  {
    color: '#00f0f0',
    name: 'bug',
  },
]

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
    body: '<!-- ## 問題点\r\n\r\ndbコンテナの`mysqld`が立ち上がる前に、flaskコンテナのアプリがdbに接続しに行っちゃう。\r\n\r\nそのため、時間を空けて別々に立ち上げないとバグる。\r\n --> \r\nhttps://github.com/knknk98/issue-twitter/pull/10#issue-678574393',
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

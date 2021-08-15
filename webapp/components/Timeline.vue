<template>
  <vue-resizable active="r" min-width="200" width="320">
    <div class="column">
      <header class="drag_handler">
        <span> <Octicon :icon="Octicons.repo" class-name="repoicon" /> </span>
        <span class="title">
          <a class="username" :href="ownerUrl" target="_blank">{{ owner }}</a>
          /
          <a class="reponame" :href="repoUrl" target="_blank">{{ repo }}</a>
        </span>
        <button class="refresh" @click="load">
          <span class="material-icons"> replay </span>
        </button>
        <button class="tune" @click="clickSettings">
          <span class="material-icons"> tune </span>
        </button>
      </header>
      <Setting
        v-show="settingOpened"
        ref="setting"
        :label-items="labelItems"
        :all-label="allLabel"
        :category-labels="categoryLabels"
        @loadTimeline="load"
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
          :add-callbacks="addCallbacks"
        ></ContentBox>
      </main>
    </div>
  </vue-resizable>
</template>

<script lang="ts">
import Vue from 'vue'
import axios from 'axios'
// @ts-ignore
import { Octicon, Octicons } from 'octicons-vue'
import { request, GraphQLClient } from 'graphql-request'
import * as gql from 'gql-query-builder'
const VueResizable = require('vue-resizable')
import { Content, Label } from '@/models/types'
import { getLabels } from '@/APIClient/labels'
import { getIssues } from '@/APIClient/issues'
import { getPullRequests } from '@/APIClient/pullRequests'
import { howLongAgo } from '@/utils/howLongAgo'
import { RefreshScheme } from '@nuxtjs/auth-next'

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
  allLabel: LabelItem
}

export default Vue.extend({
  components: { Octicon, VueResizable },
  props: {
    id: {
      type: Number,
      required: true,
    },
    owner: {
      type: String,
      required: true,
    },
    repo: {
      type: String,
      required: true,
    },
    addCallbacks: {
      type: Function,
      required: true,
    },
    columnNum: {
      type: Number,
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
    ownerUrl(): String {
      return 'https://github.com/' + this.owner
    },
    repoUrl(): String {
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

    async getIssues() {
      const states = []
      for (const categoryLabel of this.categoryLabels) {
        if (
          !categoryLabel.labelOpened &&
          ['open', 'closed'].includes(categoryLabel.label.name)
        ) {
          states.push(categoryLabel.label.name.toUpperCase())
        }
      }
      const labels = []
      for (const i in this.labelItems) {
        if (!this.labelItems[i].labelOpened) {
          labels.push(this.labelItems[i].label.name)
        }
      }
      const filter: any = {}
      if (labels.length > 0) {
        filter.labels = labels
      }

      const token: string = (this.$auth.strategy as RefreshScheme).token.get() as string
      return await getIssues(
        token,
        this.owner,
        this.repo,
        states,
        filter
      )
    },

    async getPullRequests() {
      const states = []
      for (const categoryLabel of this.categoryLabels) {
        if (
          !categoryLabel.labelOpened &&
          ['open', 'closed'].includes(categoryLabel.label.name)
        ) {
          states.push(categoryLabel.label.name.toUpperCase())
        }
      }
      const labels = []
      for (const i in this.labelItems) {
        if (!this.labelItems[i].labelOpened) {
          labels.push(this.labelItems[i].label.name)
        }
      }

      const token: string = (this.$auth.strategy as RefreshScheme).token.get() as string
      return await getPullRequests(
        token,
        this.owner,
        this.repo,
        states,
        labels
      )
    },

    getTimeline() {
      // issue, pullRequest を取得して並び替える.
      Promise.all([this.getIssues(), this.getPullRequests()])
        .then((values) => {
          const timeline = [...values[0], ...values[1]]
          timeline.sort((a, b) => {
            const keyA = a.updatedAt
            const keyB = b.updatedAt
            if (keyA > keyB) return -1
            if (keyA < keyB) return 1
            return 0
          })
          this.contents = timeline
        })
        .catch((errors) => {
          console.error(errors)
        })
    },

    getLabels() {
      const token: string = (this.$auth.strategy as RefreshScheme).token.get() as string
      getLabels(token, this.owner, this.repo)
        .then((data) => {
          this.labelItems = data
        })
        .catch((errors) => {
          console.error(errors)
        })
    },

    load() {
      this.getTimeline()
      this.getLabels()
    },

    // ラベル絞り込みボタンの開閉
    clickSettings() {
      this.settingOpened = !this.settingOpened
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
</script>

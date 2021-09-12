<template>
  <vue-resizable
    active="r"
    min-width="200"
    :width="width"
    @mount="eHandler"
    @resize:move="eHandler"
    @resize:start="eHandler"
    @resize:end="eHandler"
  >
    <div class="column">
      <header class="drag_handler">
        <span> <Octicon :icon="Octicons.repo" class-name="repoicon" /> </span>
        <span class="title">
          <a class="username" :href="ownerUrl" target="_blank">{{ owner }}</a>
          /
          <a class="reponame" :href="repoUrl" target="_blank">{{ repo }}</a>
        </span>
        <button class="refresh" @click="search">
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
          :add-callbacks="addCallbacks"
        ></ContentBox>
        <infinite-loading :identifier="infiniteId" @infinite="infiniteHandler">
          <span slot="no-more"></span>
          <span slot="no-results"></span>
        </infinite-loading>
      </main>
    </div>
  </vue-resizable>
</template>

<script lang="ts">
import Vue from 'vue'
// @ts-ignore
import { Octicon, Octicons } from 'octicons-vue'

import VueResizable from 'vue-resizable'
import InfiniteLoading from 'vue-infinite-loading'

import { Content, Issue, PullRequest, Label } from '@/models/types'
import { getLabels } from '@/APIClient/labels'
import { getIssues } from '@/APIClient/issues'
import { getPullRequests } from '@/APIClient/pullRequests'
import { RefreshScheme } from '@nuxtjs/auth-next'

type LabelItem = {
  label: Label
  labelOpened: Boolean
}

type DataType = {
  Octicons: any
  settingOpened: boolean
  contents: Array<Content>
  labelItems: Array<LabelItem>
  isLoading: boolean
  // setting から持ってきた
  categoryLabels: Array<LabelItem>
  allLabel: LabelItem

  issues: Array<Issue>
  issueHasNextPage: boolean
  issueEndCursor: string | null
  issueIndex: number
  pullRequests: Array<PullRequest>
  pullRequestHasNextPage: boolean
  pullRequestEndCursor: string | null
  pullRequestIndex: number

  infiniteId: number

  width: number
}

type VueResizablePayload = {
  width: number
}

export default Vue.extend({
  components: { Octicon, VueResizable, InfiniteLoading },
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
    addResetColumnWidthCallbacks: {
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
      issues: [],
      issueHasNextPage: true,
      issueEndCursor: null,
      issueIndex: 0,
      pullRequests: [],
      pullRequestHasNextPage: true,
      pullRequestEndCursor: null,
      pullRequestIndex: 0,
      infiniteId: 0,
      width: 320,
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
    this.getLabels()
  },
  mounted() {
    this.$props.addResetColumnWidthCallbacks(() => {
      this.resetColumnWidth()
    })
  },
  methods: {
    infiniteHandler($state: any) {
      const self = this
      this.getTimeline(() => {
        if (self.issueHasNextPage || self.pullRequestHasNextPage) {
          $state.loaded()
        } else {
          $state.complete()
        }
      })
    },

    clearContents() {
      this.issues = []
      this.issueHasNextPage = true
      this.issueEndCursor = null
      this.issueIndex = 0
      this.pullRequests = []
      this.pullRequestHasNextPage = true
      this.pullRequestEndCursor = null
      this.pullRequestIndex = 0
      this.contents = []
      this.infiniteId += 1
    },

    close() {
      this.$emit('closeTimeline', this.id)
    },

    async getIssues(endCursor: string | null = null) {
      if (!this.issueHasNextPage) {
        return {
          issues: [],
          pageInfo: {
            hasNextPage: false,
            endCursor: null,
          },
        }
      }

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

      const token: string = (
        this.$auth.strategy as RefreshScheme
      ).token.get() as string
      return await getIssues(
        token,
        this.owner,
        this.repo,
        states,
        filter,
        endCursor
      )
    },

    async getPullRequests(endCursor: string | null = null) {
      if (!this.pullRequestHasNextPage) {
        return {
          pullRequests: [],
          pageInfo: {
            hasNextPage: false,
            endCursor: null,
          },
        }
      }

      const states = []
      for (const categoryLabel of this.categoryLabels) {
        if (
          !categoryLabel.labelOpened &&
          ['open', 'closed', 'merged'].includes(categoryLabel.label.name)
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

      const token: string = (
        this.$auth.strategy as RefreshScheme
      ).token.get() as string
      return await getPullRequests(
        token,
        this.owner,
        this.repo,
        states,
        labels,
        endCursor
      )
    },

    getTimeline(callback: Function) {
      Promise.all([
        this.getIssues(this.issueEndCursor),
        this.getPullRequests(this.pullRequestEndCursor),
      ])
        .then((values) => {
          this.issues.push(...values[0].issues)
          this.issueHasNextPage = values[0].pageInfo.hasNextPage
          this.issueEndCursor = values[0].pageInfo.endCursor
          this.pullRequests.push(...values[1].pullRequests)
          this.pullRequestHasNextPage = values[1].pageInfo.hasNextPage
          this.pullRequestEndCursor = values[1].pageInfo.endCursor

          for (let k = 0; k < 100; k += 1) {
            if (this.issueIndex == this.issues.length && this.issueHasNextPage)
              break
            if (
              this.pullRequestIndex == this.pullRequests.length &&
              this.pullRequestHasNextPage
            )
              break
            if (
              this.issueIndex == this.issues.length &&
              this.pullRequestIndex == this.pullRequests.length
            )
              break
            if (
              this.pullRequestIndex == this.pullRequests.length ||
              (this.issueIndex < this.issues.length &&
                this.issues[this.issueIndex].updatedAt >
                  this.pullRequests[this.pullRequestIndex].updatedAt)
            ) {
              this.contents.push(this.issues[this.issueIndex])
              this.issueIndex += 1
            } else if (
              this.issueIndex == this.issues.length ||
              (this.pullRequestIndex < this.pullRequests.length &&
                this.issues[this.issueIndex].updatedAt <=
                  this.pullRequests[this.pullRequestIndex].updatedAt)
            ) {
              this.contents.push(this.pullRequests[this.pullRequestIndex])
              this.pullRequestIndex += 1
            }
          }
          callback()
        })
        .catch((errors) => {
          console.error(errors)
        })
    },

    getLabels() {
      const token: string = (
        this.$auth.strategy as RefreshScheme
      ).token.get() as string
      getLabels(token, this.owner, this.repo)
        .then((data) => {
          this.labelItems = data
        })
        .catch((errors) => {
          console.error(errors)
        })
    },

    search() {
      this.clearContents()
    },

    // ラベル絞り込みボタンの開閉
    clickSettings() {
      this.settingOpened = !this.settingOpened
    },
    // ラベルのON OFF管理
    clickLabel(Blockname: string, name: string) {
      // labelOpened:false->選択中
      if (Blockname === 'category') {
        const index = this.categoryLabels.findIndex(
          ({ label }) => label.name === name
        )
        this.categoryLabels[index].labelOpened =
          !this.categoryLabels[index].labelOpened
      }
      if (Blockname === 'labels') {
        const index = this.labelItems.findIndex(
          ({ label }) => label.name === name
        )
        if (index === -1) {
          if (this.allLabel.labelOpened) {
            // すべて：選択中でないときにボタン押した
            this.labelItems.map((element) => (element.labelOpened = true))
            this.allLabel.labelOpened = false
          } else {
            // this.allLabel.labelOpened = !this.allLabel.labelOpened
          }
        } else if (!this.allLabel.labelOpened) {
          this.allLabel.labelOpened = true
          this.labelItems[index].labelOpened =
            !this.labelItems[index].labelOpened
        } else {
          this.labelItems[index].labelOpened =
            !this.labelItems[index].labelOpened
          if (
            this.labelItems.every((element) => element.labelOpened === true)
          ) {
            this.allLabel.labelOpened = false
          }
        }
      }
    },
    resetColumnWidth() {
      this.width = 320
    },
    eHandler(data: VueResizablePayload) {
      this.width = data.width
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

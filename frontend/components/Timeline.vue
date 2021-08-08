<template>
  <div class="column pane">
    <header>
      <span> <Octicon :icon="Octicons.repo" class-name="repoicon" /> </span>
      <span class="title">
        <a class="username" :href="ownerUrl" target="_blank">{{ owner }}</a>
        /
        <a class="reponame" :href="repoUrl" target="_blank">{{ repo }}</a>
      </span>
      <button class="Refresh" @click="load">
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
</template>

<script lang="ts">
import Vue from 'vue'
import { Content, Label } from '@/models/types'
import axios from 'axios'
// @ts-ignore
import { Octicon, Octicons } from 'octicons-vue'
import { request, GraphQLClient } from 'graphql-request'
import * as gql from 'gql-query-builder'
import { getLabels } from '@/APIClient/labels.ts'
import { getIssues } from '@/APIClient/issues.ts'
import { getPullRequests } from '@/APIClient/pullRequests.ts'
import { howLongAgo } from '@/utils/howLongAgo.ts'

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

    async getIssues() {
      let states = []
      for (const categoryLabel of this.categoryLabels) {
        if (!categoryLabel.labelOpened && ["open", "closed"].includes(categoryLabel.label.name)) {
          states.push(categoryLabel.label.name.toUpperCase())
        }
      }
      let labels = []
      for (const i in this.labelItems) {
        if (!this.labelItems[i].labelOpened) {
          labels.push(this.labelItems[i].label.name)
        }
      }
      let filter = {}
      if (labels.length > 0) {
        filter["labels"] = labels
      }

      return await getIssues(this.$auth.getToken('github'), this.owner, this.repo, states, filter)
    },

    async getPullRequests() {
      let states = []
      for (const categoryLabel of this.categoryLabels) {
        if (!categoryLabel.labelOpened && ["open", "closed"].includes(categoryLabel.label.name)) {
          states.push(categoryLabel.label.name.toUpperCase())
        }
      }
      let labels = []
      for (const i in this.labelItems) {
        if (!this.labelItems[i].labelOpened) {
          labels.push(this.labelItems[i].label.name)
        }
      }

      return await getPullRequests(this.$auth.getToken('github'), this.owner, this.repo, states, labels)
    },

    getTimeline() {
      // issue, pullRequest を取得して並び替える.
      Promise.all([this.getIssues(), this.getPullRequests()])
        .then(values => {
          let timeline = [...values[0], ...values[1]]
          timeline.sort((a, b) => {
            let keyA = a["updatedAt"]
            let keyB = b["updatedAt"]
            if (keyA > keyB) return -1;
            if (keyA < keyB) return 1;
            return 0;
          })
          this.contents = timeline
        })
        .catch((errors) => {
          console.error(errors)
        })
    },

    getLabels() {
      getLabels(this.$auth.getToken('github'), this.owner, this.repo)
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

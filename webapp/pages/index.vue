<template>
  <div>
    <div class="container">
      <Sidebar
        ref="sidebar"
        :timeline-config="timelineConfig"
        @appendTimeline="append"
        @resetColumnWidth="resetColumnWidth"
      />
      <draggable
        v-model="timelineConfig"
        class="columns vertical-panes"
        handle=".drag_handler"
        animation="150"
      >
        <Timeline
          v-for="(tl, index) in timelineConfig"
          :id="tl.id"
          ref="timeline"
          :key="tl.id"
          :column-num="index"
          :owner="tl.owner"
          :repo="tl.repo"
          :add-callbacks="addCallbacks"
          :add-reset-column-width-callbacks="addResetColumnWidthCallbacks"
          @closeTimeline="close"
        />
      </draggable>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import draggable from 'vuedraggable'

import {
  getSavedRepository,
  removeRepositoryToLocalStorage,
} from '@/utils/localStorage'
import { checkRepository } from '@/APIClient/repository'
import { TimelineConfig } from '@/models/types'
import Timeline from '@/components/Timeline.vue'

type DataType = {
  timelineConfig: TimelineConfig[]
  addingColumnErrorMsg: String
  callbacks: Array<() => void>
  resetColumnWidthCallbacks: Array<() => void>
  test: any
}
export default Vue.extend({
  components: {
    draggable,
    Timeline,
  },
  middleware: ['auth'],
  data(): DataType {
    return {
      timelineConfig: [
        {
          owner: 'git-deck',
          repo: 'tutorial',
          id: Math.floor(Math.random() * 1000000000),
        },
      ],
      addingColumnErrorMsg: '',
      callbacks: [],
      resetColumnWidthCallbacks: [],
      test: '',
    }
  },
  created() {
    const token = this.$accessor.auth.accessToken
    if (token == null) {
      this.$router.push('/login')
      return
    }
    // localStorageからレポジトリを取得
    getSavedRepository()?.forEach((repositoryName) => {
      // TODO: 順番が保存されなさそう
      checkRepository(token, repositoryName).then(() => {
        const split = repositoryName.split('/')
        if (split.length === 2) {
          const owner: string = split[0]
          const repo: string = split[1]
          this.append(owner, repo)
        }
      })
    })
  },
  methods: {
    append(owner: string, repo: string) {
      this.timelineConfig.push({
        owner,
        repo,
        id: Math.floor(Math.random() * 1000000000),
      })
    },
    close(id: number) {
      const index = this.timelineConfig.findIndex(
        (x: TimelineConfig) => x.id === id
      )
      const reponame = `${this.timelineConfig[index].owner}/${this.timelineConfig[index].repo}`
      removeRepositoryToLocalStorage(reponame)
      this.timelineConfig.splice(index, 1)
    },
    resized() {
      this.callbacks.forEach((callback) => callback())
    },
    addCallbacks(callback: () => void) {
      this.callbacks.push(callback)
    },
    addResetColumnWidthCallbacks(callback: () => void) {
      this.resetColumnWidthCallbacks.push(callback)
    },
    resetColumnWidth() {
      this.resetColumnWidthCallbacks.forEach((callback) => callback())
    },
  },
})
</script>

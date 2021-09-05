<template>
  <div>
    <div class="container">
      <Sidebar
        ref="sidebar"
        :user-name="userName"
        :avatar-url="avatarUrl"
        :timeline-config="timelineConfig"
        @appendTimeline="append"
      />
      <div>
        <draggable
          v-model="timelineConfig"
          class="columns vertical-panes"
          handle=".drag_handler"
          animation="150"
        >
          <Timeline
            v-for="(tl, index) in timelineConfig"
            :id="tl.id"
            :key="tl.id"
            :column-num="index"
            :owner="tl.owner"
            :repo="tl.repo"
            :add-callbacks="addCallbacks"
            @closeTimeline="close"
          />
        </draggable>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import VModal from 'vue-js-modal'
import draggable from 'vuedraggable'

import { RefreshScheme } from '@nuxtjs/auth-next'
import {
  getSavedRepository,
  removeRepositoryToLocalStorage,
} from '@/utils/localStorage'
import { checkRepository } from '@/APIClient/repository'
import { TimelineConfig } from '@/models/types'

Vue.use(VModal)

type DataType = {
  timelineConfig: TimelineConfig[]
  addingColumnErrorMsg: String
  avatarUrl: String
  userName: String
  callbacks: Array<() => void>
  test: any
}
export default Vue.extend({
  components: {
    draggable,
  },
  data(): DataType {
    return {
      timelineConfig: [
        {
          owner: 'habara-k',
          repo: 'gitdeck-tutorial',
          id: Math.floor(Math.random() * 1000000000),
        },
      ],
      addingColumnErrorMsg: '',
      avatarUrl: '',
      userName: '',
      callbacks: [],
      test: '',
    }
  },
  created() {
    const user = this.$auth.user
    if (user === null) {
      throw new Error('Failed to get authorized user')
    }
    this.avatarUrl = user.avatar_url as String
    this.userName = user.login as String
    // localStorageからレポジトリを取得
    getSavedRepository().forEach((repositoryName) => {
      const token: string = (
        this.$auth.strategy as RefreshScheme
      ).token.get() as string
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
  },
})
</script>

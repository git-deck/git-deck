<template>
  <div>
    <div class="container">
      <Sidebar
        ref="sidebar"
        :user-name="userName"
        :avatar-url="avatarUrl"
        :timeline="timeline"
        @appendTimeline="append"
      />
      <div>
        <draggable
          v-model="timeline"
          class="columns vertical-panes"
          handle=".drag_handler"
          animation="150"
        >
          <Timeline
            v-for="(tl, index) in timeline"
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

import {
  getSavedRepository,
  removeRepositoryToLocalStorage,
} from '@/utils/localStorage'
import { checkRepository } from '@/APIClient/repository'
import { RefreshScheme } from '@nuxtjs/auth-next'

Vue.use(VModal)

type Timeline = {
  owner: String
  repo: String
  id: Number
}

type DataType = {
  timeline: Timeline[]
  addingColumnErrorMsg: String
  avatarUrl: String
  userName: String
  callbacks: Array<() => void>
}
export default Vue.extend({
  components: {
    draggable,
  },
  data(): DataType {
    return {
      timeline: [
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
    }
  },
  created() {
    const user = this.$auth.user
    if (user === null) {
        throw new Error("Failed to get authorized user")
        return
    }
    this.avatarUrl = (user.avatar_url as String)
    this.userName = (user.login as String)
    // localStorageからレポジトリを取得
    getSavedRepository().map((repositoryName) => {
      const token: string = (this.$auth.strategy as RefreshScheme).token.get() as string
      checkRepository(token, repositoryName).then(
        () => {
          const split = repositoryName.split('/')

          if (split.length == 2) {
            const owner: string = split[0]
            const repo: string = split[1]
            this.append(owner, repo)
          }
        }
      )
    })
  },
  methods: {
    append(owner: string, repo: string) {
      this.timeline.push({
        owner,
        repo,
        id: Math.floor(Math.random() * 1000000000),
      })
    },
    close(id: number) {
      const index = this.timeline.findIndex((x: Timeline) => x.id === id)
      const reponame = `${this.timeline[index].owner}/${this.timeline[index].repo}`
      removeRepositoryToLocalStorage(reponame)
      this.timeline.splice(index, 1)
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

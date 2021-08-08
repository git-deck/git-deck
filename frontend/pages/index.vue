<template>
  <div class="container">
    <Sidebar
      ref="sidebar"
      :user-name="userName"
      :avatar-url="avatarUrl"
      :timeline="timeline"
      @appendTimeline="append"
    />
    <multipane
      class="vertical-panes"
      layout="vertical"
      @paneResizeStop="resized"
    >
      <template v-for="(tl, index) in timeline" ref="test">
        <Timeline
          :id="tl.id"
          :key="tl.id"
          :owner="tl.owner"
          :repo="tl.repo"
          :add-callbacks="addCallbacks"
          @closeTimeline="close"
        />
        <multipane-resizer :key="index + 'resizer'"></multipane-resizer>
      </template>
    </multipane>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import VModal from 'vue-js-modal'
import axios from 'axios'
import { Multipane, MultipaneResizer } from 'vue-multipane'
import {
  getSavedRepository,
  removeRepositoryToLocalStorage,
} from '@/utils/localStorage.ts'
import { checkRepository } from '@/APIClient/repository.ts'

axios.defaults.baseURL = 'http://localhost:5000'

Vue.use(VModal)

type DataType = {
  timeline: Object[]
  addingColumnErrorMsg: String
  avatarUrl: String
  userName: String
  callbacks: Array<() => void>
}
export default Vue.extend({
  components: {
    Multipane,
    MultipaneResizer,
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
    this.avatarUrl = this.$auth.user.avatar_url
    this.userName = this.$auth.user.login
    // localStorageからレポジトリを取得
    getSavedRepository().map((repositoryName) =>
      checkRepository(this.$auth.getToken('github'), repositoryName).then(() => {
        this.append(...repositoryName.split('/'))
      })
    )
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
      const index = this.timeline.findIndex((x) => x.id === id)
      const reponame = `${this.timeline[index].owner}/${this.timeline[index].repo}`
      removeRepositoryToLocalStorage(reponame)
      this.timeline.splice(index, 1)
    },
    resized() {
      this.callbacks.forEach((callback) => callback())
    },
    addCallbacks(callback) {
      this.callbacks.push(callback)
    },
  },
})
</script>

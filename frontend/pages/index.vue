<template>
  <div class="container">
    <Sidebar
      ref="sidebar"
      :user-name="userName"
      :avatar-url="avatarUrl"
      @appendTimeline="append"
    />
    <PostModal ref="postmodal" />
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
          :use-dummy-data="tl.useDummyData"
          @closeTimeline="close"
          @openPostModal="openPostModal"
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
          owner: 'knknk98',
          repo: 'issue-twitter',
          useDummyData: true,
          id: Math.floor(Math.random() * 1000000000),
        },
        {
          owner: 'knknk98',
          repo: 'issue-twitter',
          useDummyData: true,
          id: Math.floor(Math.random() * 1000000000),
        },
        {
          owner: 'knknk98',
          repo: 'issue-twitter',
          useDummyData: true,
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
      this.timeline.splice(index, 1)
    },
    openPostModal(owner: string, repo: string) {
      this.$refs.postmodal.showModal(owner, repo)
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

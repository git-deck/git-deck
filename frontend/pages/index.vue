<template>
  <div class="container">
    <Sidebar
      ref="sidebar"
      :user-name="userName"
      :avatar-url="avatarUrl"
      @appendTimeline="append"
    />
    <PostModal ref="postmodal"/>
    <multipane class="vertical-panes" layout="vertical">
      <template v-for="(tl, index) in timeline">
        <Timeline
          :id="index"
          :key="index + 'timeline'"
          :owner="tl.owner"
          :repo="tl.repo"
          :useDummyData="tl.useDummyData"
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
        },
        {
          owner: 'knknk98',
          repo: 'issue-twitter',
          useDummyData: true,
        },
        {
          owner: 'knknk98',
          repo: 'issue-twitter',
          useDummyData: true,
        },
      ],
      addingColumnErrorMsg: '',
      avatarUrl: '',
      userName: '',
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
      })
    },
    close(id: number) {
      this.timeline.splice(id, 1)
    },
    openPostModal(owner: string, repo: string) {
      this.$refs.postmodal.showModal(owner, repo)
    }
  },
})
</script>

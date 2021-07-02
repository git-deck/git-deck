<template>
  <div class="container">
    <Sidebar
      ref="sidebar"
      :avatar-url="$auth.state.user.avatar_url"
      @appendTimeline="append"
    />
    <Timeline
      v-for="(tl, index) in timeline"
      :key="index"
      :owner="tl.owner"
      :repo="tl.repo"
      :useDummyData="tl.useDummyData"
    />
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import VModal from 'vue-js-modal'
import axios from 'axios'

axios.defaults.baseURL = 'http://localhost:5000'

Vue.use(VModal)

type DataType = {
  timeline: Object[]
  addingColumnErrorMsg: String
}
export default Vue.extend({
  data(): DataType {
    return {
      timeline: [
        {
          owner: 'knknk98',
          repo: 'issue-twitter',
          useDummyData: true,
        },
      ],
      addingColumnErrorMsg: '',
    }
  },
  methods: {
    append(owner: string, repo: string) {
      this.timeline.push({
        owner,
        repo,
      })
    },
  },
})
</script>

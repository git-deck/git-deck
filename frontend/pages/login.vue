<template>
  <div class="container">ログイン画面</div>
</template>

<script lang="ts">
import Vue from 'vue'
import VModal from 'vue-js-modal'

Vue.use(VModal)

type DataType = {
  timeline: Object[]
}
export default Vue.extend({
  data(): DataType {
    return {
      timeline: [
        {
          owner: 'knknk98',
          repo: 'issue-twitter',
          ownerUrl: 'https://github.com/knknk98',
          repoUrl: 'https://github.com/knknk98/issue-twitter',
        },
        {
          owner: 'knknk98',
          repo: 'issue-twitter',
          ownerUrl: 'https://github.com/knknk98',
          repoUrl: 'https://github.com/knknk98/issue-twitter',
        },
      ],
    }
  },
  methods: {
    append(owner: string, repo: string) {
      this.timeline.push({
        owner,
        repo,
        ownerUrl: 'https://github.com/' + owner,
        repoUrl: 'https://github.com/' + owner + '/' + repo,
      })
    },
  },
})
</script>

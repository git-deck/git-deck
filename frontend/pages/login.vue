<template>
  <div class="container">
    <div class="login-page">
      <div class="caption">
        <div class="title">
          <span>GitDeck</span>
          <span><img class="cat-icon" :src="catIcon" alt="" /></span>
        </div>
        <div class="subtext">
          <p>
            GitHubの通知は分散しすぎてわからない！そんなあなたに向けたサービスです
          </p>
          <p>
            複数リポジトリの通知をタイムラインに表示したり、issueにも満たないアイデアも投稿できます
          </p>
        </div>
      </div>
      <div class="login-button">
        <div class="caption">Login with Your GitHub account</div>
        <button @click="loginWithGitHub">
          <Octicon :icon="Octicons.markGithub" class-name="github-mark" />Log in
        </button>
        <div class="link">
          New to GitHub?
          <a href="https://github.com/signup" target="_blank">Sign up now »</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import CatIcon from '@/assets/img/cat.svg'

const { Octicon, Octicons } = require('octicons-vue')
type DataType = {
  Octicons: any
  catIcon: String
}
export default Vue.extend({
  components: { Octicon },
  data(): DataType {
    return {
      Octicons,
      catIcon: CatIcon,
    }
  },
  methods: {
    loginWithGitHub() {
      console.log('this:', this)
      console.log('this.$auth:', this.$auth)
      this.$auth.loginWith('github')
    },
  },
})
</script>

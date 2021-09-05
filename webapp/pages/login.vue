<template>
  <div class="container">
    <div class="login-page">
      <div class="caption">
        <div class="title">
          <span>GitDeck</span>
          <span><img class="cat-icon" src="@/assets/img/cat.svg" /></span>
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
      <div class="footer">
        <p>supported by "今日もいっぱい汗角蔵"</p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
// @ts-ignore
import { Octicon, Octicons } from 'octicons-vue'
type DataType = {
  Octicons: any
}
export default Vue.extend({
  components: { Octicon },
  data(): DataType {
    return {
      Octicons,
    }
  },
  methods: {
    loginWithGitHub() {
      this.$auth.loginWith('github')
    },
  },
})
</script>

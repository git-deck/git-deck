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
            複数のリポジトリのIssue/Pull
            Requestやそこで行われている議論を一目でチェックすることができます。
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
          <a
            href="https://github.com/signup"
            target="_blank"
            rel="noopener noreferrer"
            >Sign up now »</a
          >
        </div>
      </div>
      <div class="footer">
        <p>&copy; 今日もいっぱい汗角蔵</p>
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
  middleware: ['unauth'],
  data(): DataType {
    return {
      Octicons,
    }
  },
  created() {
    if (this.$accessor.auth.isLoggedIn) {
      this.$router.push('/')
    }
  },
  methods: {
    loginWithGitHub() {
      try {
        // NOTE: 直前にURLを変更することでfirebaseのリダイレクト先を`/`にする
        history.pushState({}, '', '/')
        const provider = new this.$fireModule.auth.GithubAuthProvider()
        provider.addScope('repo')
        this.$fire.auth.signInWithRedirect(provider)
      } catch (e) {
        console.error(e)
        alert('エラーが発生しました')
      }
    },
  },
})
</script>

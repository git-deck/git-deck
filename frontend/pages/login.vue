<template>
  <div class="container">
    <div class="login-page">
      <div class="caption">
        <div class="title">GitDeck</div>
        <div class="subtext">
          いい感じの説明が入リますいい感じの説明が入リますいい感じの説明が入リますいい感じの説明が入リますいい感じの説明が入リますいい感じの説明が入リます
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

const { Octicon, Octicons } = require('octicons-vue')
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
      console.log('this:', this)
      console.log('this.$auth:', this.$auth)
      this.$auth.loginWith('github')
    },
  },
})
</script>

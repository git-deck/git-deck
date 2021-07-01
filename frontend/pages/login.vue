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
        <div class="caption">Login with GitHub account</div>
        <button>
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
})
</script>

<template>
  <div class="comment">
    <Icon class="icon" />
    <div class="contents">
      <span class="title">チャット画面UIの実装</span>
      <span class="number">#245</span>
      <div class="assign">
        <Icon class="assigner" /> <Icon class="assigner" /><Icon
          class="assigner"
        />
        ...
      </div>
      <div class="labels">
        <span class="label">bug</span>
        <span class="label">backend</span>
        <span class="label">frontend</span>
        <span class="label">good first issue</span>
      </div>
      <div class="text"></div>
    </div>
    <Octicon :icon="Octicons.gitPullRequest" class-name="comment-type-mark" />
    <div class="date">2日</div>
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

<template>
  <div class="comment">
    <div class="iconItem">
      <Icon class="icon" />
      <div class="thread-line"></div>
    </div>
    <div class="titleItem">
      <span class="title">チャット画面UIの実装</span>
      <span class="number">#245</span>
      <div class="assign">
        <Icon class="assigner" /> <Icon class="assigner" /><Icon
          class="assigner"
        />
        ...
      </div>
    </div>
    <div class="markItem">
      <Octicon :icon="Octicons.gitPullRequest" class-name="comment-type-mark" />
    </div>
    <div class="dateItem">2日</div>
    <div class="textItem">
      <div class="text">ああああああああああ</div>
      <div class="labels">
        <span class="label">bug</span>
        <span class="label">backend</span>
        <span class="label">frontend</span>
        <span class="label">good first</span>
      </div>
      <div class="readmore">このスレッドを全て表示</div>
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

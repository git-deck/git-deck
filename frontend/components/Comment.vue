<template>
  <div class="comment">
    <div class="iconItem">
      <Icon :class="type" />
      <div v-if="thread" class="thread-line"></div>
    </div>
    <div class="titleItem">
      <span class="title">チャット画面UIの実装</span>
      <span v-if="(type === 'issue') | (type === 'pullRequest')" class="number"
        >#245</span
      >
      <div v-if="(type === 'issue') | (type === 'pullRequest')" class="assign">
        <Icon class="assigner" /> <Icon class="assigner" /><Icon
          class="assigner"
        />
        ...
      </div>
    </div>
    <div class="markItem">
      <Octicon
        v-if="type === 'pullRequest'"
        :icon="Octicons.gitPullRequest"
        class-name="comment-type-mark pull-request"
      />
      <Octicon
        v-if="type === 'issue'"
        :icon="Octicons.issueOpened"
        class-name="comment-type-mark issue"
      />
      <Octicon
        v-if="type === 'idea'"
        :icon="Octicons.lightBulb"
        class-name="comment-type-mark idea"
      />
    </div>
    <div class="dateItem">2日</div>
    <div class="textItem">
      <div v-if="(type === 'reply') | (type === 'idea')" class="text">
        ああああああああああ
      </div>
      <div v-if="type === 'issue'" class="labels">
        <span class="label">bug</span>
        <span class="label">backend</span>
        <span class="label">frontend</span>
        <span class="label">good first</span>
      </div>
      <div
        v-if="(type === 'issue') | (type === 'pullRequest') && thread"
        class="readmore"
      >
        このスレッドを全て表示
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
  props: {
    type: {
      type: String,
      required: true,
    },
    thread: {
      type: Boolean,
      default: false,
    },
  },
  data(): DataType {
    return {
      Octicons,
    }
  },
})
</script>

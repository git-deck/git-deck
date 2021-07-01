<template>
  <div
    class="comment"
    :class="{
      thread: thread,
    }"
  >
    <div class="iconItem">
      <Icon :class="type" />
      <div v-if="thread" class="thread-line"></div>
    </div>
    <div class="titleItem">
      <span class="title">{{ title }}</span>
      <span v-if="(type === 'issue') | (type === 'pullRequest')" class="number"
        >#{{ number }}</span
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
    <div class="dateItem">{{ howLongAgo }}</div>
    <div class="textItem">
      <div v-if="(type === 'reply') | (type === 'idea')" class="text">
        {{ body }}
      </div>
      <div v-if="type === 'issue' || type === 'pullRequest'" class="labels">
        <Label
          v-for="(label, index) in labels"
          :key="index"
          :message="label.name"
          :color="label.color"
        />
      </div>
      <div
        v-if="(type === 'issue' || type === 'pullRequest') && thread"
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
    title: {
      type: String,
      default: 'チャット画面UIの実装',
    },
    number: {
      type: Number,
      default: 245,
    },
    body: {
      type: String,
      default: 'あああ〜ああ〜ああ',
    },
    howLongAgo: {
      type: String,
      default: '2日',
    },
    labels: {
      type: Array,
      default() {
        return [
          {
            name: 'bug',
          },
          {
            name: 'backend',
          },
          {
            name: 'frontend',
          },
          {
            name: 'good first',
          },
        ]
      },
    },
  },
  data(): DataType {
    return {
      Octicons,
    }
  },
})
</script>

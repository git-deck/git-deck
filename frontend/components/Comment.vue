<template>
  <div
    class="comment"
    :class="{
      thread: thread,
    }"
  >
    <div class="iconItem">
      <Icon :avatar-url="author.avatarUrl" :class="type" />
      <div v-if="thread" class="thread-line"></div>
    </div>
    <div class="titleItem">
      <span class="title">{{ title }}</span>
      <span v-if="(type === 'issue') | (type === 'pullRequest')" class="number"
        >#{{ number }}</span
      >
      <div v-if="(type === 'issue') | (type === 'pullRequest')" class="assign">
        <Icon
          v-for="(assignee, index) in assignees.slice(0, 3)"
          :key="index"
          :avatar-url="assignee.avatarUrl"
          class="assigner"
        />
        {{ assignees.length > 3 ? '...' : '' }}
      </div>
    </div>
    <div class="markItem">
      <Octicon
        v-if="type === 'pullRequest' && state === 'OPEN'"
        :icon="Octicons.gitPullRequest"
        class-name="comment-type-mark pull-request-open"
      />
      <Octicon
        v-if="type === 'pullRequest' && state === 'CLOSED'"
        :icon="Octicons.gitPullRequest"
        class-name="comment-type-mark pull-request-closed"
      />
      <Octicon
        v-if="type === 'pullRequest' && state === 'MERGED'"
        :icon="Octicons.gitPullRequest"
        class-name="comment-type-mark pull-request-merged"
      />
      <Octicon
        v-if="type === 'issue' && state === 'OPEN'"
        :icon="Octicons.issueOpened"
        class-name="comment-type-mark issue-open"
      />
      <Octicon
        v-if="type === 'issue' && state === 'CLOSED'"
        :icon="Octicons.issueOpened"
        class-name="comment-type-mark issue-closed"
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
        <div v-html="$md.render(body)"></div>
      </div>
      <div v-if="type === 'issue' || type === 'pullRequest'" class="labels">
        <Label
          v-for="(label, index) in labels"
          :key="index"
          :message="label.name"
          :color="label.color"
        />
      </div>
      <a
        v-if="
          (type === 'issue' || type === 'pullRequest') && thread && readmore
        "
        :href="url"
        target="_blank"
        class="readmore"
      >
        このスレッドを全て表示
      </a>
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
    state: {
      type: String,
      default: 'OPEN',
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
    author: {
      type: Object,
      default() {
        return {
          login: 'habara-k',
          avatarUrl: 'https://github.com/knknk98.png',
          url: 'https://github.com/knknk98',
        }
      },
    },
    url: {
      type: String,
      default: 'https://github.com/',
    },
    readmore: {
      type: Boolean,
      default: false,
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
    assignees: {
      type: Array,
      default() {
        return [
          {
            avatarUrl: 'https://github.com/habara-k.png',
          },
          {
            avatarUrl: 'https://github.com/knknk98.png',
          },
          {
            avatarUrl: 'https://github.com/zwwaa-ku.png',
          },
          {
            avatarUrl: 'https://github.com/yuta-ike.png',
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

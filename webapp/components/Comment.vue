<template>
  <div
    class="comment"
    :class="{
      reply: type === 'reply',
      thread: thread,
    }"
  >
    <div class="iconItem">
      <Icon
        :avatar-url="author == null ? '' : author.avatarUrl"
        :class="type"
      />
      <div v-if="thread" class="thread-line"></div>
    </div>
    <div
      v-if="readmore || fold"
      class="threadLine"
      :class="{ dotted: readmore }"
    ></div>
    <div class="titleItem">
      <div v-if="(type === 'issue') | (type === 'pullRequest')">
        <a :href="url" target="_blank" class="titleLine">
          <h1 class="title">
            {{ title }}
            <span
              v-if="(type === 'issue') | (type === 'pullRequest')"
              class="number"
              >#{{ number }}</span
            >
          </h1>
        </a>
      </div>
      <div v-else class="titleLine">
        <h1 class="title">
          {{ title }}
          <span
            v-if="(type === 'issue') | (type === 'pullRequest')"
            class="number"
            >#{{ number }}</span
          >
        </h1>
      </div>
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
    <div class="dateItem">{{ howLongAgo }}</div>
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
        :icon="Octicons.gitMerge"
        class-name="comment-type-mark pull-request-merged"
      />
      <Octicon
        v-if="type === 'issue' && state === 'OPEN'"
        :icon="Octicons.issueOpened"
        class-name="comment-type-mark issue-open"
      />
      <Octicon
        v-if="type === 'issue' && state === 'CLOSED'"
        :icon="Octicons.issueClosed"
        class-name="comment-type-mark issue-closed"
      />
      <Octicon
        v-if="type === 'idea'"
        :icon="Octicons.lightBulb"
        class-name="comment-type-mark idea"
      />
    </div>
    <div ref="textarea" class="textItem" :style="{ height: textHeight }">
      <div v-if="type === 'issue' || type === 'pullRequest'" class="labels">
        <Label
          v-for="(label, index) in labels"
          :key="index"
          :message="label.name"
          :color="label.color"
        />
      </div>
      <div class="textItemCon" v-html="$md.render(body)"></div>
    </div>
    <button
      v-if="height > MAX_COMMENT_HEIGT"
      class="buttonItem"
      @click="LongCommentClick"
    >
      {{ buttonMark }}
    </button>
    <div v-if="readmore" class="readmoreItem">
      <a class="readmore" @click="$emit('toggleShowingAll')">
        返信をさらに表示
      </a>
    </div>
    <div v-if="fold" class="readmoreItem">
      <a class="readmore" @click="$emit('toggleShowingAll')">
        返信を折り畳む
      </a>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
// @ts-ignore
import { Octicon, Octicons } from 'octicons-vue'
type DataType = {
  Octicons: any
  height: Number
  isLongCommentOpened: boolean
  MAX_COMMENT_HEIGT: Number
}
export default Vue.extend({
  components: { Octicon },
  props: {
    addCallbacks: {
      type: Function,
      required: true,
    },
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
    fold: {
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
      height: 0,
      isLongCommentOpened: false,
      MAX_COMMENT_HEIGT: 350,
    }
  },
  computed: {
    showReadMoreIcon() {
      return (
        (this.type === 'issue' || this.type === 'pullRequest') &&
        this.thread &&
        this.readmore
      )
    },
    textHeight(): string {
      if (!this.isLongCommentOpened && this.height > this.MAX_COMMENT_HEIGT) {
        return '100px'
      } else {
        return '100%'
      }
    },
    buttonMark(): string {
      if (this.isLongCommentOpened) {
        return '▲'
      } else {
        return '▼'
      }
    },
  },
  mounted() {
    this.$props.addCallbacks(() => {
      if (this.$refs.textarea != null) {
        const tmp = this.$refs.textarea.clientHeight
        this.height = tmp
      }
    })
    if (this.$refs.textarea != null) {
      const tmp = this.$refs.textarea.clientHeight
      this.height = tmp
    }
  },
  methods: {
    LongCommentClick() {
      this.isLongCommentOpened = !this.isLongCommentOpened
    },
  },
})
</script>

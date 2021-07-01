<template>
  <div>
    <div v-if="content.category == 'idea'">
      <Comment
        :title="content.author.login"
        :body="content.body"
        :author="content.author"
        :how-long-ago="content.howLongAgo"
        :type="'idea'"
        :state="content.state"
      />
    </div>
    <div v-else>
      <Comment
        :title="content.title"
        :number="content.number"
        :labels="content.labels"
        :assignees="content.assignees"
        :body="content.body"
        :author="content.author"
        :how-long-ago="content.howLongAgo"
        :thread="content.comments.length > 0"
        :type="content.category"
        :state="content.state"
        :readmore="readmore"
      />
      <Comment
        v-for="(comment, index) in lessComments"
        :key="index"
        :title="comment.author.login"
        :body="comment.body"
        :author="comment.author"
        :how-long-ago="comment.howLongAgo"
        :type="'reply'"
        :thread="index + 1 < lessComments.length"
      />
    </div>
  </div>
</template>

<script lang="ts">
import Vue, { PropOptions } from 'vue'
import { Content } from '@/models/types'

export default Vue.extend({
  props: {
    content: {
      type: Object,
      required: true,
    } as PropOptions<Content>,
  },
  computed: {
    readmore() {
      return this.content.comments.length > 2
    },
    lessComments() {
      const len = this.content.comments.length
      return this.content.comments.slice(len >= 2 ? len - 2 : 0, len)
    },
  },
})
</script>

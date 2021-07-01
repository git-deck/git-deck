<template>
  <div>
    <div v-if="content.category == 'idea'">
      <Comment
        :title="content.author.login"
        :body="content.body"
        :author="content.author"
        :how-long-ago="content.howLongAgo"
        :type="'idea'"
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
      />
      <Comment
        v-for="(comment, index) in content.comments"
        :key="index"
        :title="content.author.login"
        :body="comment.body"
        :author="content.author"
        :how-long-ago="comment.howLongAgo"
        :type="'reply'"
        :thread="index + 1 < content.comments.length"
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
})
</script>

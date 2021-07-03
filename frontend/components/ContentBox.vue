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
      <div v-if="showingAll">
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
          :fold="content.comments.length > 2"
          :url="content.url"
          @toggleShowingAll="toggleShowingAll"
        />
        <Comment
          v-for="(comment, index) in content.comments"
          :key="index"
          :title="comment.author.login"
          :body="comment.body"
          :author="comment.author"
          :how-long-ago="comment.howLongAgo"
          :type="'reply'"
          :thread="index + 1 < content.comments.length"
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
          :readmore="content.comments.length > 2"
          :url="content.url"
          @toggleShowingAll="toggleShowingAll"
        />
        <Comment
          v-for="(comment, index) in content.comments.slice(
            content.comments.length >= 2 ? content.comments.length - 2 : 0,
            content.comments.length
          )"
          :key="index"
          :title="comment.author.login"
          :body="comment.body"
          :author="comment.author"
          :how-long-ago="comment.howLongAgo"
          :type="'reply'"
          :thread="index + 1 < Math.min(content.comments.length, 2)"
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue, { PropOptions } from 'vue'
import { Content } from '@/models/types'


export default Vue.extend({
  name: 'ContentBox',
  props: {
    content: {
      type: Object,
      required: true,
    } as PropOptions<Content>,
  },
  data() {
    return {
      showingAll: false,
    }
  },
  methods: {
    toggleShowingAll() {
      this.showingAll = !this.showingAll
    },
  },
})
</script>

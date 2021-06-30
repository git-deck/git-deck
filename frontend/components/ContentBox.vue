<template>
  <div>
    <div v-if="content.category == 'idea'">
      <Comment
        :title="content.author.login"
        :body="content.body"
        :howLongAgo="content.howLongAgo"
        :type="'idea'"
      />
    </div>
    <div v-else>
      <Comment
        :title="content.title"
        :number="content.number"
        :labels="content.labels"
        :body="content.body"
        :howLongAgo="content.howLongAgo"
        :thread="content.comments.length > 0"
        :type="content.category"
      ></Comment>
      <Comment
        v-for="(comment, index) in content.comments"
        :key="index"
        :title="content.author.login"
        :body="comment.body"
        :howLongAgo="comment.howLongAgo"
        :type="'reply'"
        :thread="index + 1 < content.comments.length"
      ></Comment>
    </div>
  </div>
</template>

<script lang="ts">
import Vue, { PropOptions } from 'vue'
import { Content } from '@/models/types'
const { Octicon, Octicons } = require('octicons-vue')
type DataType = {
  Octicons: any
}
export default Vue.extend({
  components: { Octicon },
  props: {
    content: {
      type: Object,
      required: true,
    } as PropOptions<Content>,
  },
  data(): DataType {
    return {
      Octicons,
    }
  },
})
</script>

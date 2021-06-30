<template>
  <div>
    <div v-if="content.category='idea'">
      <Comment type='idea'/>
    </div>
    <div v-if="content.category='issue'">
      <Comment type='issue'/>
    </div>
    <div v-if="content.category='pullRequest'">
      <Comment type='pullRequest'/>
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
    } as PropOptions<Content>
  },
  data(): DataType {
    return {
      Octicons,
    }
  },
})
</script>

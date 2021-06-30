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
import Vue from 'vue'
const { Octicon, Octicons } = require('octicons-vue')
type DataType = {
  Octicons: any
}
export default Vue.extend({
  components: { Octicon },
  props: {
    content: Object
  },
  data(): DataType {
    return {
      Octicons,
    }
  },
})
</script>

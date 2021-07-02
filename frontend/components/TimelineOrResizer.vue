<template v-if="type === 'resizer'">
  <multipane-resizer></multipane-resizer>
</template>


<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  props: {
    type: {
      type: String,
      required: true,
    },
    id: {
      type: Number,
      required: true,
    },
    useDummyData: {
      type: Boolean,
      default: false,
    },
    owner: {
      type: String,
      required: true,
    },
    repo: {
      type: String,
      required: true,
    },
  },
})
</script>

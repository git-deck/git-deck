<template>
  <span v-bind:style="{ background: color }" class="label">
    {{ message }}
  </span>
</template>
<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  name: 'Label',
  props: {
    color: {
      type: String,
    },
    message: {
      type: String,
    },
  },
})
</script>
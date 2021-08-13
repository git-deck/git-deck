<template>
  <img class="user-icon" :src="avatarUrl" alt="icon" />
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  props: {
    avatarUrl: {
      type: String,
      default: 'https://github.com/github.png',
    },
  },
})
</script>

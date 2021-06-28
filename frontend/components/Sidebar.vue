<template>
  <div class="sidebar">
    <button @click="showModal">
      <span class="material-icons"> add </span>
    </button>
    <button>
      <Icon />
    </button>
    <modal name="column-modal">カラム追加画面</modal>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  methods: {
    showModal() {
      this.$modal.show('column-modal')
    },
  },
})
</script>

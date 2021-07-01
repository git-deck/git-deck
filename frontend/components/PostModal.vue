<template>
  <modal name="editor-modal" :click-to-close="false" :draggable="true">
    <div class="modal-content">
      <div class="header">
        <div class="topic">アイデアを投稿する</div>
        <button @click="hideModal">
          <span class="material-icons">close</span>
        </button>
      </div>
      <div class="main-contents">
        <div class="repo">to knknk98/reporeporepo</div>
        <textarea></textarea>
        <button>投稿する</button>
      </div>
    </div></modal
  >
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  methods: {
    showModal() {
      this.$modal.show('editor-modal')
    },
    hideModal() {
      this.$modal.hide('editor-modal')
    },
  },
})
</script>

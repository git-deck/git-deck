<template>
  <div class="sidebar">
    <div class="menu">
      <button @click="showModal">
        <span class="material-icons"> add </span>
      </button>
      <button>
        <Icon />
      </button>
    </div>
    <modal name="column-modal" :click-to-close="false" :draggable="true">
      <div class="modal-content">
        <div class="header">
          <div class="topic">カラムを追加する</div>
          <button @click="hideModal">
            <span class="material-icons">close</span>
          </button>
        </div>
        <div class="main-contents">
          <div>追加したいリポジトリ名を入力してください</div>
          <input placeholder="username/repository" size="50%" /><button
            @click="append"
          >
            追加
          </button>
        </div>
      </div>
    </modal>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  methods: {
    showModal() {
      this.$modal.show('column-modal')
    },
    hideModal() {
      this.$modal.hide('column-modal')
    },
    append() {
      const owner = 'knknk98'
      const repo = 'issue-twitter'
      this.$emit('appendTimeline', owner, repo)
      this.hideModal()
    },
  },
})
</script>

<template>
  <div class="column">
    <header>
      <span class="repoicon">
        <Octicon :icon="Octicons.repo" />
      </span>
      <span class="title"
        ><a class="username" href="https://github.com/knknk98/">knknk98/</a
        ><a class="reponame" href="https://github.com/knknk98/sushi-chat/"
          >sushi-sushi-sushi-sushi-sushi-sushi-sushi-sushi-</a
        ></span
      >
      <button @click="showModal">
        <span class="material-icons chat"> chat_bubble_outline </span>
      </button>
      <button @click="clickSettings">
        <span class="material-icons tune"> tune </span>
      </button>
    </header>
    <modal name="editor-modal">投稿画面</modal>
    <div v-if="settingOpened" class="settings"></div>

    <main>main</main>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
const { Octicon, Octicons } = require('octicons-vue')

type DataType = {
  Octicons: any
  settingOpened: boolean
}

export default Vue.extend({
  components: { Octicon },
  data(): DataType {
    return {
      Octicons,
      settingOpened: false,
    }
  },
  methods: {
    // ラベル絞り込みボタンの開閉
    clickSettings() {
      this.settingOpened = !this.settingOpened
    },
    showModal() {
      this.$modal.show('editor-modal')
    },
  },
})
</script>

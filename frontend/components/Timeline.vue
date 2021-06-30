<template>
  <div class="column">
    <header>
      <span> <Octicon :icon="Octicons.repo" class-name="repoicon" /> </span>
      <span class="title"
        ><a class="username" href="https://github.com/knknk98/">knknk98/</a
        ><a class="reponame" href="https://github.com/knknk98/sushi-chat/"
          >sushi-sushi-sushi</a
        ></span
      >
      <button class="chat" @click="showModal">
        <span class="material-icons"> chat_bubble_outline </span>
      </button>
      <button class="tune" @click="clickSettings">
        <span class="material-icons"> tune </span>
      </button>
    </header>
    <modal name="editor-modal">投稿画面</modal>
    <Setting v-if="settingOpened" />
    <main>
      <Comment type="pullRequest" thread="true" />
      <Comment type="reply" thread="true" />
      <Comment type="reply" thread="true" />
      <Comment type="reply" />
      <Comment type="issue" />
      <Comment type="idea" />
    </main>
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

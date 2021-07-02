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
        <textarea v-model="ideaBody"></textarea>
        <div v-if="errorMsg != ''" style="color: red">{{ errorMsg }}</div>
        <button @click="append">投稿する</button>
      </div>
    </div></modal
  >
</template>

<script lang="ts">
import Vue from 'vue'
import axios from 'axios'

axios.defaults.baseURL = 'http://localhost:5000'

type DataType = {
  ideaBody: String
  errorMsg: String
}

export default Vue.extend({
  props: {
    owner: {
      type: String,
      required: true,
    },
    repo: {
      type: String,
      required: true,
    },
  },
  data(): DataType {
    return {
      ideaBody: '',
      errorMsg: '',
    }
  },
  methods: {
    showModal() {
      this.$modal.show('editor-modal')
    },
    hideModal() {
      this.$modal.hide('editor-modal')
      this.errorMsg = ''
    },
    append() {
      const self = this
      if (self.ideaBody === '') {
        self.errorMsg = '本文を入力してください'
        return
      }
      axios.post(
        '/ideas',
        JSON.stringify({
          owner: self.owner,
          repo: self.repo,
          body: self.ideaBody,
          author_login: self.$auth.state.user.login,
        }),
        {
          headers: {
            'Content-Type': 'application/json',
            Authorization: self.$auth.getToken('github'),
          },
        }
      )
      this.hideModal()
    },
  },
})
</script>

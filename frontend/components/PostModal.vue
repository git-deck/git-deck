<template>
  <modal name="post-modal" :click-to-close="false" :draggable="true">
    <div class="modal-content">
      <div class="header">
        <div class="topic">アイデアを投稿する</div>
        <button @click="hideModal">
          <span class="material-icons">close</span>
        </button>
      </div>
      <div class="main-contents">
        <div class="repo">
          to <span class="address">{{ owner }}/{{ repo }}</span>
        </div>
        <textarea v-model="ideaBody" v-focus class="postTextBox"></textarea>
        <div v-if="errorMsg != ''" style="color: red">{{ errorMsg }}</div>
        <button class="postButton" @click="append">
          投稿する
          <Octicon
            :icon="Octicons.lightBulb"
            class-name="comment-type-mark idea"
          />
        </button>
      </div>
    </div>
  </modal>
</template>

<script lang="ts">
import Vue from 'vue'
import { Octicon, Octicons } from 'octicons-vue'
import axios from 'axios'

axios.defaults.baseURL = 'http://localhost:5000'

type DataType = {
  Octicons: any
  ideaBody: String
  errorMsg: String
  owner: String
  repo: String
}
Vue.directive('focus', {
  // ひも付いている要素が DOM に挿入される時...
  inserted(el) {
    // 要素にフォーカスを当てる
    el.focus()
  },
})

export default Vue.extend({
  name: 'PostModal',
  components: { Octicon },
  data(): DataType {
    return {
      Octicons,
      ideaBody: '',
      errorMsg: '',
      owner: '',
      repo: '',
    }
  },
  methods: {
    hideModal() {
      this.$modal.hide('post-modal')
      this.errorMsg = ''
    },
    showModal(owner: string, repo: string) {
      this.owner = owner
      this.repo = repo
      this.$modal.show('post-modal')
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

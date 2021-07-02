<template>
  <div class="sidebar">
    <div class="menu">
      <button @click="clickMyAvatar">
        <Icon :avatar-url="avatarUrl" />
      </button>
      <button class="add-button" @click="showModal">
        <span class="material-icons"> add </span>
      </button>
    </div>
    <div v-if="isOpenedPulldownMenu" class="pulldown-menu">
      <p class="header">
        Signed in as
        <span class="user-name">{{ userName }}</span>
      </p>
      <button @click="logout">Log out</button>
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
          <label for="repository-input" class="repositoryInputLabel"
            >追加したいリポジトリ名を入力してください</label
          >
          <input
            id="repository-input"
            v-model="repositoryInput"
            placeholder="owner/repository"
            class="inputField"
            size="50%"
          />
          <div v-if="errorMsg != ''" style="color: red">{{ errorMsg }}</div>
          <button class="addButton" @click="append">追加</button>
        </div>
      </div>
    </modal>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import axios from 'axios'

axios.defaults.baseURL = 'http://localhost:5000'

type DataType = {
  repositoryInput: String
  errorMsg: String
  isOpenedPulldownMenu: Boolean
}

export default Vue.extend({
  props: {
    userName: {
      type: String,
      required: true,
    },
    avatarUrl: {
      type: String,
      required: true,
    },
  },
  data(): DataType {
    return {
      repositoryInput: '',
      errorMsg: '',
      isOpenedPulldownMenu: false,
    }
  },
  methods: {
    showModal() {
      this.$modal.show('column-modal')
    },
    hideModal() {
      this.$modal.hide('column-modal')
      this.repositoryInput = ''
      this.errorMsg = ''
    },
    setErrorMsg(errorMsg: string) {
      this.errorMsg = errorMsg
    },
    append() {
      const parsed = this.repositoryInput.match(
        /([a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38})/gi
      )
      console.log('parsed:', parsed)
      if (parsed == null || parsed.length < 2) {
        this.setErrorMsg('入力形式が正しくありません')
      } else {
        const owner = parsed[0]
        const repo = parsed[1]
        const self = this
        axios
          .get('/repo_id/' + owner + '/' + repo, {
            headers: {
              Authorization: self.$auth.getToken('github'),
            },
          })
          .then((response) => {
            console.log('response:', response)
            this.$emit('appendTimeline', parsed[0], parsed[1])
            this.hideModal()
          })
          .catch((error) => {
            console.log('error:', error)
            this.setErrorMsg('リポジトリが見つかりません')
          })
      }
    },
    clickMyAvatar() {
      this.isOpenedPulldownMenu = !this.isOpenedPulldownMenu
    },
    logout() {
      this.$auth.logout()
    },
  },
})
</script>

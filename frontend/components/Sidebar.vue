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
            >追加したいリポジトリ名またはURLを入力してください</label
          >
          <input
            id="repository-input"
            v-model="repositoryInput"
            v-focus
            placeholder="owner/repository"
            class="inputField"
            size="50%"
            @paste="onPaste"
            @paste.prevent
          />
          <div v-if="errorMsg != ''" style="color: red">{{ errorMsg }}</div>
          <button
            class="addButton"
            :disabled="isSearchingRepository"
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
import axios from 'axios'
import { addRepository } from '@/APIClient/repository.ts'
import { saveRepositoryToLocalStorage } from '@/utils/localStorage.ts'

axios.defaults.baseURL = 'http://localhost:5000'

type DataType = {
  repositoryInput: String
  errorMsg: String
  isOpenedPulldownMenu: Boolean
  isSearchingRepository: Boolean
}
Vue.directive('focus', {
  // ひも付いている要素が DOM に挿入される時...
  inserted(el) {
    // 要素にフォーカスを当てる
    el.focus()
  },
})
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
    timeline: {
      type: Array,
      required: true,
    },
  },

  data(): DataType {
    return {
      repositoryInput: '',
      errorMsg: '',
      isOpenedPulldownMenu: false,
      isSearchingRepository: false,
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
    updateValue(e) {
      this.repositoryInput = e.target.value
    },
    onPaste(e) {
      const input = e.clipboardData.getData('text')
      if (input != null && typeof input === 'string') {
        const res = input.match(
          /^https:\/\/github\.com\/(?<owner>.+)\/(?<repo>.+)/
        )
        if (res?.groups?.repo != null && res?.groups?.owner != null) {
          this.repositoryInput += `${res.groups.owner}/${res.groups.repo}`
        } else {
          this.repositoryInput += input
        }
      }
    },
    async append() {
      this.isSearchingRepository = true
      const res = this.repositoryInput.match(
        /^https:\/\/github\.com\/(?<owner>.+)\/(?<repo>.+)/
      )
      let parsed = []
      if (res?.groups?.repo != null && res?.groups?.owner != null) {
        parsed = ['', res.groups.owner, res.groups.repo]
      } else {
        parsed = this.repositoryInput.match(/^([^/]+)\/([^/]+)$/)
      }
      console.log('parsed:', parsed)

      console.log(this.timeline)

      if (parsed == null || parsed.length < 3) {
        this.setErrorMsg('入力形式が正しくありません')
        this.isSearchingRepository = false
      } else if (
        this.timeline.find(
          ({ owner, repo }) => owner === parsed[1] && repo === parsed[2]
        )
      ) {
        this.setErrorMsg('既に登録済みのレポジトリです')
      } else {
        const owner = parsed[1]
        const repo = parsed[2]
        const self = this
        try {
          const res = await addRepository(
            self.$auth.getToken('github'),
            `${owner}/${repo}`
          )
          console.log('response:', res)
          this.$emit('appendTimeline', owner, repo)
          saveRepositoryToLocalStorage(`${owner}/${repo}`)
          this.hideModal()
        } catch (e) {
          console.log('error:', e)
          this.setErrorMsg('リポジトリが見つかりません')
        } finally {
          self.isSearchingRepository = false
        }
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

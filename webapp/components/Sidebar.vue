<template>
  <div class="sidebar">
    <div class="menu">
      <button @click="clickMyAvatar">
        <Icon :avatar-url="avatarUrl" />
      </button>
      <div class="sidebar-button">
        <button style="padding-bottom: 0" @click="showModal('settings')">
          <span class="material-icons"> settings </span>
        </button>
        <button style="padding-top: 0" @click="showModal('column-modal')">
          <span class="material-icons"> add </span>
        </button>
      </div>
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
          <button @click="hideModal('column-modal')">
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
    <modal name="settings" :click-to-close="false" :draggable="true">
      <div class="modal-content">
        <div class="header">
          <div class="topic">設定画面</div>
          <button @click="hideModal('settings')">
            <span class="material-icons">close</span>
          </button>
        </div>
        <div class="main-contents">
          <p>カラーモード</p>
          <select v-model="$colorMode.preference">
            <option value="system">System</option>
            <option value="light">Light</option>
            <option value="dark">Dark</option>
          </select>
        </div>
      </div>
    </modal>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from 'vue'
import { checkRepository } from '@/APIClient/repository'
import { TimelineConfig } from '@/models/types'
import { saveRepositoryToLocalStorage } from '@/utils/localStorage'
import { RefreshScheme } from '@nuxtjs/auth-next'

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
    timelineConfig: {
      type: Array as PropType<Array<TimelineConfig>>,
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
    showModal(name: string) {
      this.$modal.show(name)
    },
    hideModal(name: string) {
      this.$modal.hide(name)
      this.repositoryInput = ''
      this.errorMsg = ''
    },
    setErrorMsg(errorMsg: string) {
      this.errorMsg = errorMsg
    },
    onPaste(e: ClipboardEvent) {
      if (e.clipboardData == null) return
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
      let parsed: Array<String> | null = []
      if (res?.groups?.repo != null && res?.groups?.owner != null) {
        parsed = ['', res.groups.owner, res.groups.repo]
      } else {
        parsed = this.repositoryInput.match(/^([^/]+)\/([^/]+)$/)
      }

      if (parsed == null || parsed.length < 3) {
        this.setErrorMsg('入力形式が正しくありません')
        this.isSearchingRepository = false
        return
      }

      const owner: String = parsed[1]
      const repo: String = parsed[2]

      // 既に登録済みのリポジトリを追加しない
      if (this.timelineConfig.some((tl: TimelineConfig) => (tl.owner === owner && tl.repo === repo))) {
        return
      }

      const self = this
      try {
        const token: string = (this.$auth.strategy as RefreshScheme).token.get() as string
        const res = await checkRepository(
          token,
          `${owner}/${repo}`
        )
        this.$emit('appendTimeline', owner, repo)
        saveRepositoryToLocalStorage(`${owner}/${repo}`)
        this.hideModal('column-modal')
      } catch (error) {
        console.error(error)
        this.setErrorMsg('リポジトリが見つかりません')
      } finally {
        self.isSearchingRepository = false
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
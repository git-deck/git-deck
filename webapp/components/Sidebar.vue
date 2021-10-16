<template>
  <div class="sidebar">
    <div class="menu">
      <button @click="clickMyAvatar">
        <Icon :avatar-url="authUser.avaterUrl" />
      </button>
      <div class="sidebar-button">
        <button style="padding-bottom: 0" @click="showModal('settings')">
          <span class="material-icons settings"> settings </span>
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
    <modal
      name="column-modal"
      :click-to-close="false"
      :draggable="true"
      height="auto"
      class="column-add-modal"
    >
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
          <fieldset class="inputFieldset">
            <input
              id="repository-input"
              v-model="repositoryInput"
              v-focus
              list="my-repositories"
              autocomplete="on"
              autofocus
              placeholder="owner/repository または URL"
              class="inputField"
              size="50%"
              @paste="onPaste"
              @paste.prevent
            />
            <datalist id="my-repositories">
              <option
                v-for="repository in myRepositories"
                :key="repository.owner + '/' + repository.name"
                :value="repository.owner + '/' + repository.name"
              ></option>
            </datalist>
          </fieldset>
          <hr class="separator" />
          <p>または自分のレポジトリから選ぶ</p>
          <div class="repository-recommend hide-scrollbar">
            <button
              v-for="repository in myRepositories.slice(0, 5)"
              :key="repository.owner + '/' + repository.name"
              class="recommended-button"
              :class="{
                selected:
                  repositoryInput === repository.owner + '/' + repository.name,
              }"
              :aria-pressed="
                repositoryInput === repository.owner + '/' + repository.name
              "
              @click="
                repositoryInput = repository.owner + '/' + repository.name
              "
            >
              {{ repository.owner + '/' + repository.name }}
            </button>
            <label
              class="recommended-button show-all-button"
              :class="{
                selected:
                  othersSelectedRepository === repositoryInput &&
                  othersSelectedRepository !== '',
              }"
            >
              <select
                v-model="othersSelectedRepository"
                @change="repositoryInput = $event.target.value"
              >
                <option value="">他のリポジトリ</option>
                <option
                  v-for="repository in myRepositories"
                  :key="repository.owner + '/' + repository.name"
                  :value="repository.owner + '/' + repository.name"
                >
                  {{ repository.owner + '/' + repository.name }}
                </option>
              </select>
            </label>
          </div>
          <div style="color: red">{{ errorMsg }}</div>
          <button
            class="addButton"
            :disabled="isSearchingRepository || !inputIsValid"
            @click="append"
          >
            追加
          </button>
        </div>
      </div>
    </modal>
    <modal name="settings" :click-to-close="false">
      <div class="modal-content">
        <div class="header">
          <div class="topic">設定画面</div>
          <button @click="hideModal('settings')">
            <span class="material-icons">close</span>
          </button>
        </div>
        <div class="main-contents">
          <p>カラーモード</p>
          <label class="setting-button">
            <select v-model="$colorMode.preference">
              <option value="system">System</option>
              <option value="light">Light</option>
              <option value="dark">Dark</option>
            </select>
          </label>
          <p>カラム</p>
          <div class="setting-button">
            <button @click="$emit('resetColumnWidth')">
              カラムをデフォルトの幅に戻す
            </button>
          </div>
          <p>
            お問い合わせは<a
              href="https://forms.gle/yJQT8uy4qRCHfjtG7"
              target="_blank"
              rel="noopener noreferrer"
              >こちら</a
            >から
          </p>
        </div>
      </div>
    </modal>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import type { PropType } from 'vue'
import { checkRepository, getMyRepositories } from '@/APIClient/repository'
import { AuthUser, TimelineConfig } from '@/models/types'
import { saveRepositoryToLocalStorage } from '@/utils/localStorage'

type DataType = {
  repositoryInput: string
  errorMsg: string
  isOpenedPulldownMenu: boolean
  isSearchingRepository: boolean
  myRepositories: { owner: string; name: string }[]
  othersSelectedRepository: string
}
Vue.directive('focus', {
  // ひも付いている要素が DOM に挿入される時...
  inserted(el) {
    // 要素にフォーカスを当てる
    el.focus()
  },
})
export default Vue.extend({
  name: 'Sidebar',
  props: {
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
      myRepositories: [],
      othersSelectedRepository: '',
    }
  },
  computed: {
    authUser(): AuthUser {
      return this.$accessor.auth.authUser as AuthUser
    },
    userName(): string | null {
      return this.$accessor.auth.userName
    },
    inputIsValid(): boolean {
      const res = this.repositoryInput.match(
        /^https:\/\/github\.com\/(?<owner>.+)\/(?<repo>.+)/
      )

      return (
        (res?.groups?.repo != null && (res?.groups?.owner != null) == null) ||
        /^([^/]+)\/([^/]+)$/.test(this.repositoryInput)
      )
    },
  },
  watch: {
    async userName() {
      const token = this.$accessor.auth.accessToken
      if (token != null && this.userName != null) {
        this.myRepositories = await getMyRepositories(token, this.userName)
      }
    },
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
      if (this.repositoryInput.length === 0) {
        this.setErrorMsg('リポジトリ名またはURL入力してください')
        this.isSearchingRepository = false
        return
      }

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
      if (
        this.timelineConfig.some(
          (tl: TimelineConfig) => tl.owner === owner && tl.repo === repo
        )
      ) {
        return
      }

      const self = this
      try {
        const token = this.$accessor.auth.accessToken
        if (token == null) {
          return
        }
        await checkRepository(token, `${owner}/${repo}`)
        saveRepositoryToLocalStorage(`${owner}/${repo}`)
        this.$emit('appendTimeline', owner, repo)
        this.hideModal('column-modal')
      } catch (error) {
        if (
          error?.response?.errors?.find((e: any) => e?.type === 'NOT_FOUND') !=
          null
        ) {
          console.log(error.response.errors)
          console.error(error?.response.errors)
          this.setErrorMsg('リポジトリが見つかりません')
        } else {
          this.setErrorMsg('エラーが発生しました')
        }
      } finally {
        self.isSearchingRepository = false
      }
    },
    clickMyAvatar() {
      this.isOpenedPulldownMenu = !this.isOpenedPulldownMenu
    },
    async logout() {
      try {
        await this.$fire.auth.signOut()
        this.$router.push('/login')
      } catch (e) {
        console.error(e)
        alert('エラーが発生しました')
      }
    },
  },
})
</script>

<template>
  <div class="sidebar">
    <div class="menu">
      <button>
        <Icon />
      </button>
      <button class="add-button" @click="showModal">
        <span class="material-icons"> add </span>
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
          <label for="repository-input" class="repositoryInputLabel"
            >追加したいリポジトリ名を入力してください</label
          >
          <input
            id="repository-input"
            v-model="repositoryInput"
            placeholder="username/repository"
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

type DataType = {
  repositoryInput: String
  errorMsg: String
}

export default Vue.extend({
  data(): DataType {
    return {
      repositoryInput: '',
      errorMsg: '',
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
        this.$emit('appendTimeline', parsed[0], parsed[1])
        //this.hideModal()
      }
    },
  },
})
</script>

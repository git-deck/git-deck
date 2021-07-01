<template>
  <div class="column">
    <header>
      <span> <Octicon :icon="Octicons.repo" class-name="repoicon" /> </span>
      <span class="title"
        ><a class="username" :href="ownerUrl">{{ owner }}</a
        >/<a class="reponame" :href="repoUrl">{{ repo }}</a></span
      >
      <button class="chat" @click="showModal">
        <span class="material-icons"> chat_bubble_outline </span>
      </button>
      <button class="tune" @click="clickSettings">
        <span class="material-icons"> tune </span>
      </button>
    </header>
    <PostModal />
    <Setting v-if="settingOpened" />
    <main>
      <ContentBox
        v-for="(content, index) in contents"
        :key="index"
        :content="content"
      ></ContentBox>
    </main>
  </div>
</template>

<script lang="ts">
import Vue, { PropOptions } from 'vue'
import { Content } from '@/models/types'

const { Octicon, Octicons } = require('octicons-vue')

type DataType = {
  Octicons: any
  settingOpened: boolean
}

export default Vue.extend({
  components: { Octicon },
  props: {
    contents: {
      type: Array,
      required: true,
    } as PropOptions<Content[]>,
    owner: {
      type: String,
      required: true,
    },
    repo: {
      type: String,
      required: true,
    },
    ownerUrl: {
      type: String,
      required: true,
    },
    repoUrl: {
      type: String,
      required: true,
    },
  },
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

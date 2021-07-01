<template>
  <span style="cursor: pointer" class="labelButton" @click="clickLabel">
    <Label :color="getLabelColor(labelOpened)" :message="sendmessage"></Label>
  </span>
</template>
<script lang="ts">
import Vue from 'vue'
import Label from '@/components/Label.vue'

type DataType = {
  labelOpened: boolean
  sendcolor: string
  sendmessage: string
}

export default Vue.extend({
  name: 'LabelToButton',
  components: {
    Label: Label,
  },
  props: {
    color: {
      type: String,
      required: true,
    },
    message: {
      type: String,
      required: true,
    },
  },
  data(): DataType {
    return {
      labelOpened: true,
      sendcolor: '#bbbbbb',
      sendmessage: this.message,
    }
  },
  methods: {
    // ラベル絞り込みボタンの開閉
    getLabelColor(getlabelOpened: boolean) {
      return this.labelOpened ? this.color : '#dddddd'
    },
    clickLabel() {
      this.labelOpened = !this.labelOpened
    },
  },
})
</script>

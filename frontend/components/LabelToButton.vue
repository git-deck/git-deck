<template>
  <span style="cursor: pointer" class="labelButton" @click="clickLabel">
    <Label :color="color" :message="message" :disabled="!labelOpened"></Label>
  </span>
</template>
<script lang="ts">
import Vue from 'vue'
import Label from '@/components/Label.vue'

type DataType = {
  labelOpened: boolean
}

export default Vue.extend({
  name: 'LabelToButton',
  components: {
    Label,
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
    }
  },
  methods: {
    clickLabel() {
      this.labelOpened = !this.labelOpened
    },
  },
})
</script>

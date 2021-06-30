<template>
  <div class="label_column">
    <header>
      <button class="filter_list">
        <span class="material-icons"> filter_list </span>
      </button>
      <span class="m">ラベルで絞り込む</span>

      <div class="labels">
        <Label :color="color" :message="message" />
      </div>
    </header>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

type DataType = {
  color: string
  message: string
}
export default Vue.extend({
  data(): DataType {
    return {
      color: '#ff0f00',
      message: 'ex_label',
    }
  },
})
</script>

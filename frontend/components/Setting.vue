<template>
  <div class="label_column">
    <header>
      <button class="filter_list" @click="clickSettings">
        <span class="material-icons"> filter_list </span>
      </button>
      <span class="m">ラベルで絞り込む</span>

      <div class="labels">
        <Label :color="color" :message="message"></Label>
      </div>
    </header>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import Label from '@/components/Lavel.vue'
type DataType = {
  style: string
  message: string
}
export default Vue.extend({
  components: {
    Label,
  },
  data() {
    return {
      color: '#ff0f00',
      message: 'ex_label',
    }
  },
})
</script>
<template>
  <div class="label_column">
    <button class="filter_list">
      <span class="material-icons"> filter_list </span>
    </button>
    <span class="filter_message">ラベルで絞り込む</span>

    <div v-for="item in items" :key="item.color" class="labels">
      <Label :color="item.color" :message="item.message"></Label>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import Label from '@/components/Label.vue'
export default Vue.extend({
  components: {
    Label: Label,
  },
  data() {
    return {
      items: [
        {
          // numberが識別子
          number: 1,
          color: '#ff0f00',
          message: 'label',
        },
        {
          number: 2,
          color: '#00ffff',
          message: 'bug',
        },
      ],
    }
  },
})
</script>

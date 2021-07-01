<template>
  <div class="label_column">
    <header>
      <div class="top">
        <button class="filter_list">
          <span class="material-icons"> filter_list </span>
        </button>

        <span class="filter_message">ラベルで絞り込む</span>

        <button class="Refresh">
          <span class="material-icons"> replay </span>
        </button>
      </div>
      <div class="labels">
        <LabelToButton
          v-for="(item, index) in items"
          :key="index"
          :color="item.color"
          :message="item.message"
        ></LabelToButton>
      </div>
      <div class="bottom">
        <button class="Refresh">
          <span class="material-icons"> close </span>
        </button>

        <span class="message">このカラムを削除</span>
      </div>
    </header>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import LabelToButton from '@/components/LabelToButton.vue'
export default Vue.extend({
  components: {
    LabelToButton: LabelToButton,
  },
  data() {
    return {
      items: [
        {
          // numberが識別子
          color: '#ff0f00',
          message: 'label',
        },
        {
          color: '#00ffff',
          message: 'bug',
        },
      ],
    }
  },
})
</script>

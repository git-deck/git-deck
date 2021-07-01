<template>
  <div class="label_column">
    <header>
      <div class="top">
        <div class="filterbutton">
          <button class="filter_list">
            <span class="material-icons"> filter_list </span>
          </button>
          <span class="filter_message">ラベルで絞り込む</span>
        </div>
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
    </header>
    <div class="bottom">
      <div class="bottomContent">
        <div class="right">
          <button class="Close">
            <span class="material-icons"> close </span>
          </button>
          <span class="message">このカラムを削除</span>
        </div>
      </div>
    </div>
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
          color: '#ff0000',
          message: 'すべて',
        },
        {
          // numberが識別子
          color: '#ff0f00',
          message: 'label',
        },
        {
          color: '#00ffff',
          message: 'bug',
        },
        {
          color: '#0000ff',
          message: 'bug',
        },
        {
          color: '#00ff00',
          message: 'bug',
        },
        {
          color: '#00f0f0',
          message: 'bug',
        },
        {
          color: '#0000ff',
          message: 'bug',
        },
        {
          color: '#00ff00',
          message: 'ggggggggggggggggggggggggggggggggggggggggggg',
        },
        {
          color: '#00f0f0',
          message: 'bug',
        },
      ],
    }
  },
})
</script>

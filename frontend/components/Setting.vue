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
        <button class="Refresh" @click="$emit('loatTimeline')">
          <span class="material-icons"> replay </span>
        </button>
      </div>
      <div class="labels">
        <LabelToButton
          v-for="(label, index) in items"
          :key="index"
          :color="label.color"
          :message="label.name"
        ></LabelToButton>
      </div>
      <div class="labels">
        <LabelToButton
          v-for="(label, index) in labels"
          :key="index"
          :color="label.color"
          :message="label.name"
        ></LabelToButton>
      </div>
    </header>
    <div class="bottom">
      <div class="bottomContent">
        <div class="right">
          <button class="Close" @click="$emit('closeTimeline')">
            <span class="material-icons"> close </span>
          </button>
          <span class="message">このカラムを削除</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue, { PropOptions } from 'vue'
import { Label } from '@/models/types'
import LabelToButton from '@/components/LabelToButton.vue'
export default Vue.extend({
  components: {
    LabelToButton,
  },
  props: {
    labels: {
      type: Array,
      required: true,
    } as PropOptions<Label[]>,
  },
  data() {
    return {
      items: [
        {
          // numberが識別子
          color: '#ffffff',
          name: 'idea',
        },
        {
          // numberが識別子
          color: '#ff0000',
          name: 'issue & pull request',
        },
      ],
    }
  },
})
</script>

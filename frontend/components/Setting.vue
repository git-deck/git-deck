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
      </div>

      <div class="categoryBlock">
        <div id="categoryBlockmes" style="font-size: 12px; color: gray">
          カテゴリ
        </div>
        <div class="Lab">
          <span
            v-for="(label, index) in categoryLabels"
            :key="index"
            class="labels"
            style="cursor: pointer"
            @click="$emit('clickLabel', 'category', index)"
          >
            <Label0
              :color="label.label.color"
              :message="label.label.name"
              :disabled="label.labelOpened"
            ></Label0>
          </span>
        </div>
      </div>
      <div clas="labelsBlock">
        <div id="labelsBlockmes" style="font-size: 12px; color: gray">
          ラベル
        </div>
        <div class="Lab">
          <span
            class="labels"
            style="cursor: pointer"
            @click="$emit('clickLabel', 'labels', -1)"
          >
            <Label0
              :color="allLabel.label.color"
              :message="allLabel.label.name"
              :disabled="allLabel.labelOpened"
            ></Label0>
          </span>
          <span
            v-for="(label, index) in labelItems"
            :key="index"
            class="labels"
            style="cursor: pointer"
            @click="$emit('clickLabel', 'labels', index)"
          >
            <Label0
              :color="label.label.color"
              :message="label.label.name"
              :disabled="label.labelOpened"
            ></Label0>
          </span>
        </div>
      </div>
    </header>
    <div class="bottom">
      <div class="bottomContent">
        <div class="bottomright">
          <div class="closetooltip">
            <a class="closemessage" @click="$emit('closeTimeline')">
              このカラムを削除
            </a>
            <div class="description">カラムを削除します</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue, { PropOptions } from 'vue'
import { Label } from '@/models/types'
import Label0 from '@/components/Label.vue'
type LabelItem = {
  label: Label
  labelOpened: Boolean
}
export default Vue.extend({
  components: {
    Label0,
  },
  props: {
    categoryLabels: {
      type: Array,
      required: true,
    } as PropOptions<LabelItem[]>,
    allLabel: {
      type: Object,
      required: true,
    } as PropOptions<LabelItem>,
    labelItems: {
      type: Array,
      required: true,
    } as PropOptions<LabelItem[]>,
  },
})
</script>

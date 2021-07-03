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
        <button class="Refresh" @click="$emit('loadTimeline')">
          <span class="material-icons"> replay </span>
        </button>
      </div>

      <div class="categoryBlock">
        <div id="categoryBlockmes" style="font-size: 12px; color: gray">
          カテゴリ
        </div>
        <div class="Lab">
          <span
            v-for="(label, index) in categoryitems"
            :key="index"
            class="labels"
            style="cursor: pointer"
            @click="clickLabel('category', index)"
          >
            <Label0
              :color="label.color"
              :message="label.name"
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
            @click="clickLabel('labels', -1)"
          >
            <Label0
              :color="allLabel.color"
              :message="allLabel.name"
              :disabled="allLabel.labelOpened"
            ></Label0>
          </span>
          <span
            v-for="(label, index) in labelsitems"
            :key="index"
            class="labels"
            style="cursor: pointer"
            @click="clickLabel('labels', index)"
          >
            <Label0
              :color="label.color"
              :message="label.name"
              :disabled="label.labelOpened"
            ></Label0>
          </span>
        </div>
      </div>
    </header>
    <div class="bottom">
      <div class="bottomContent">
        <div class="right">
          <a class="message" @click="$emit('closeTimeline')">
            このカラムを削除
          </a>
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
  name: String
  color: String
  labelOpened: Boolean
}
type DataType = {
  labelsitems: Array<LabelItem>
  categoryitems: Array<LabelItem>
  allLabel: Label
}
export default Vue.extend({
  components: {
    Label0,
  },
  props: {
    labels: {
      type: Array,
      required: true,
    } as PropOptions<Label[]>,
  },
  data(): DataType {
    return {
      allLabel: {
        name: 'すべて',
        color: '#24292E',
        labelOpened: false,
      },
      labelsitems: this.labels.map((element: Label) => ({
        name: element.name,
        color: element.color,
        labelOpened: true,
      })),
      categoryitems: [
        {
          // numberが識別子
          color: '#FFB800',
          name: 'idea',
          labelOpened: false,
        },
        {
          // numberが識別子
          color: '#2EA44F',
          name: 'issue & pull request',
          labelOpened: false,
        },
      ],
    }
  },
  methods: {
    clickLabel(Blockname: string, index: number) {
      // labelOpened:false->選択中
      if (Blockname === 'category') {
        this.categoryitems[index].labelOpened =
          !this.categoryitems[index].labelOpened
      }
      if (Blockname === 'labels') {
        if (index === -1) {
          if (this.allLabel.labelOpened) {
            // すべて：選択中でないときにボタン押した
            this.labelsitems.map((element) => (element.labelOpened = true))
            this.allLabel.labelOpened = false
          } else {
            this.allLabel.labelOpened = !this.allLabel.labelOpened
          }
        } else if (!this.allLabel.labelOpened) {
          this.allLabel.labelOpened = !this.allLabel.labelOpened
          this.labelsitems[index].labelOpened =
            !this.labelsitems[index].labelOpened
        } else {
          this.labelsitems[index].labelOpened =
            !this.labelsitems[index].labelOpened
        }
      }
    },
  },
})
</script>

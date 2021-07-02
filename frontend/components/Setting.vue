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
        <button class="Refresh" @click="refresh">
          <span class="material-icons"> replay </span>
        </button>
      </div>

      <div class="categoryBlock">
        <div class="mes">カテゴリ</div>
        <div class="Lab">
          <div
            v-for="(label, index) in categoryitems"
            :key="index"
            class="labels"
          >
            <span
              style="cursor: pointer"
              class="labelButton"
              v-on:click="clickLabel('category', index)"
            >
              <Label0
                :color="label.color"
                :message="label.name"
                :disabled="label.labelOpened"
              ></Label0>
            </span>
          </div>
        </div>
      </div>
      <div clas="labelsBlock">
        <div class="mes">ラベル</div>
        <div class="Lab">
          <div
            v-for="(label, index) in labelsitems"
            :key="index"
            class="labels"
          >
            <span
              style="cursor: pointer"
              class="labelButton"
              v-on:click="clickLabel('labels', index)"
            >
              <Label0
                :color="label.color"
                :message="label.name"
                :disabled="label.labelOpened"
              ></Label0>
            </span>
          </div>
        </div>
      </div>
    </header>
    <div class="bottom">
      <div class="bottomContent">
        <button class="Close">
          <span class="material-icons"> close </span>
        </button>
        <span class="message">このカラムを削除</span>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue, { PropOptions } from 'vue'
import { Label } from '@/models/types'
import Label0 from '@/components/Label.vue'
type DataType = {
  labelsitems: Array<Object>
  categoryitems: Array<Object>
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
  data() {
    return {
      labelsitems: this.labels.map((element: Label) => ({
        name: element.name,
        color: element.color,
        labelOpened: false,
      })),
      categoryitems: [
        {
          // numberが識別子
          color: '#ffffff',
          name: 'idea',
          labelOpened: false,
        },
        {
          // numberが識別子
          color: '#ff0000',
          name: 'issue & pull request',
          labelOpened: false,
        },
      ],
    }
  },
  methods: {
    refresh() {
      this.$emit('loatTimeline')
    },
    clickLabel: function (Blockname: string, index: number) {
      if (Blockname == 'category') {
        this.categoryitems[index].labelOpened =
          !this.categoryitems[index].labelOpened
      }
      if (Blockname == 'labels') {
        this.labelsitems[index].labelOpened =
          !this.labelsitems[index].labelOpened
      }
    },
  },
})
</script>

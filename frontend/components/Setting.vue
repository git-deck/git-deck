<template>
  <div class="label_column">
    <header>
      <div class="categoryBlock">
        <div class="categoryBlockmes">カテゴリ</div>
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
      <div class="labelsBlock">
        <div class="labelsBlockmes">ラベル</div>
        <div class="Lab">
          <span
            v-if="!allLabel.labelOpened"
            class="labels"
            style="cursor: pointer"
            @click="$emit('clickLabel', 'labels', -1)"
          >
            <Label0
              :color="allLabel.label.color"
              :message="allLabel.label.name"
            ></Label0>
          </span>
          <span
            v-for="(label, index) in checkedlabelItems"
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
        <LabelSearchBox
          :label-items="labelItems"
          :all-label="allLabel"
          @clickLabel="handle"
        ></LabelSearchBox>
      </div>
    </header>
    <div class="bottom">
      <div class="bottomContent">
        <a class="closemessage" @click="$emit('closeTimeline')">
          このカラムを削除
        </a>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue, { PropOptions } from 'vue'
import { Label } from '@/models/types'
import Label0 from '@/components/Label.vue'
import LabelSearchBox from '@/components/LabelSearchBox.vue'
type LabelItem = {
  label: Label
  labelOpened: boolean
}
export default Vue.extend({
  components: {
    Label0,
    LabelSearchBox,
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
  computed: {
    checkedlabelItems() {
      return this.labelItems.filter((label) => !label.labelOpened)
    },
  },
  methods: {
    handle(...args) {
      this.$emit('clickLabel', ...args)
    },
  },
})
</script>

<template>
  <div class="search">
    <input
      v-model="value"
      type="text"
      class="search-box"
      placeholder="ラベルを検索"
    />
    <div class="options">
      <button
        v-if="value.length === 0"
        class="label-option all-select"
        @click="() => $emit('clickLabel', 'labels', null)"
      >
        全て選択する
      </button>
      <button
        v-for="label in labels"
        :key="label.label.name"
        class="label-option"
        @click="() => $emit('clickLabel', 'labels', label.label.name)"
      >
        <span
          class="material-icons"
          :class="{ hide: label.labelOpened && allLabel.labelOpened }"
        >
          done
        </span>
        <span
          class="circle-badge"
          :style="{ background: label.label.color }"
        ></span>
        <span
          class="label-content"
          :class="{ checked: label.labelOpened && allLabel.labelOpened }"
        >
          {{ label.label.name }}
        </span>
      </button>
    </div>
  </div>
</template>
<script lang="ts">
import Vue, { PropOptions } from 'vue'
import { Label } from '@/models/types'
import compareWithDistance from '@/utils/sortWithDistance'

type LabelItem = {
  label: Label
  labelOpened: boolean
}

export default Vue.extend({
  props: {
    labelItems: {
      type: Array,
      required: true,
    } as PropOptions<LabelItem[]>,
    allLabel: {
      type: Object,
      required: true,
    } as PropOptions<LabelItem>,
  },
  data() {
    return {
      value: '',
    }
  },
  computed: {
    labels(): any {
      // eslint-disable-next-line vue/no-mutating-props, vue/no-side-effects-in-computed-properties
      return this.labelItems.sort((a: LabelItem, b: LabelItem) => {
        // if (a.labelOpened && !b.labelOpened) {
        //   return -1
        // } else if (!a.labelOpened && b.labelOpened) {
        //   return 1
        // } else if (!a.labelOpened && !b.labelOpened) {
        //   return 0
        // }
        return compareWithDistance(this.value)(a.label.name, b.label.name)
      })
    },
  },
})
</script>

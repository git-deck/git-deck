<template>
  <span class="labelBlock">
    <span
      :style="{
        border: getBooleanByColor(color) ? bordercss : '',
        backgroundColor: disabled ? 'rgb(197 197 197)' : color,
        color: disabled ? 'white' : getColorByBgColor(color),
      }"
      class="label"
    >
      {{ message }}
    </span>
  </span>
</template>
<style scoped>
.label {
  box-sizing: border-box;
}
</style>
<script lang="ts">
import Vue from 'vue'
type DataType = {
  bordercss: any
}
export default Vue.extend({
  name: 'Label',
  data(): DataType {
    return {
      bordercss: 'solid 0.5px rgb(197,197,197)',
    }
  },
  props: {
    color: {
      type: String,
      required: true,
    },
    message: {
      type: String,
      required: true,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    getColorByBgColor(hexcolor: string) {
      const r = parseInt(hexcolor.substr(1, 2), 16)
      const g = parseInt(hexcolor.substr(3, 2), 16)
      const b = parseInt(hexcolor.substr(5, 2), 16)
      return (r * 299 + g * 587 + b * 114) / 1000 < 128 ? 'white' : 'black'
    },
    getBooleanByColor(hexcolor: string) {
      const r = parseInt(hexcolor.substr(1, 2), 16)
      const g = parseInt(hexcolor.substr(3, 2), 16)
      const b = parseInt(hexcolor.substr(5, 2), 16)
      return r + g + b > 650 ? true : false
    },
  },
})
</script>

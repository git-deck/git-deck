<template>
  <span
    :style="{
      border: getBooleanByColor(color) ? bordercss : '',
      backgroundColor: disabled ? 'rgb(197 197 197)' : color,
      color: disabled ? 'white' : getColorByBgColor(color),
    }"
    class="label"
    :class="{ disabled }"
  >
    {{ message }}
  </span>
</template>
<script lang="ts">
import Vue from 'vue'
type DataType = {
  bordercss: any
}
export default Vue.extend({
  name: 'Label',
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
  data(): DataType {
    return {
      bordercss: 'solid 0.2px rgb(197,197,197)',
    }
  },
  methods: {
    getColorByBgColor(hexcolor: string) {
      const r = parseInt(hexcolor.substr(1, 2), 16)
      const g = parseInt(hexcolor.substr(3, 2), 16)
      const b = parseInt(hexcolor.substr(5, 2), 16)
      return (r * 249 + g * 587 + b * 134) / 1000 < 172 ? 'white' : 'black'
    },
    getBooleanByColor(hexcolor: string) {
      const r = parseInt(hexcolor.substr(1, 2), 16)
      const g = parseInt(hexcolor.substr(3, 2), 16)
      const b = parseInt(hexcolor.substr(5, 2), 16)
      // この条件分の閾値を変えれば枠線の付く色の種類を変えれる
      return r + g + b > 650
    },
  },
})
</script>
<style scoped></style>

<template>
  <span
    :style="{
      border: getBooleanByColor() ? 'solid 0.2px ' + borderColor : 'none',
      backgroundColor: disabled ? 'rgb(197 197 197)' : backgroundColor,
      color: disabled ? 'white' : textColor,
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
  r: number
  g: number
  b: number
  isWhiteTextMode: boolean
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
      r: 0,
      g: 0,
      b: 0,
      isWhiteTextMode: true,
    }
  },
  computed: {
    backgroundColor(): string {
      if (this.$colorMode.value === 'dark') {
        if (this.isWhiteTextMode) {
          return this.rgb(this.r / 3, this.g / 1.5, this.b / 1.5)
        } else {
          return this.rgb(this.r * 0.5, this.g * 0.5, this.b * 0.5)
        }
      } else {
        return this.color
      }
    },
    borderColor(): string {
      if (this.$colorMode.value === 'dark') {
        if (this.isWhiteTextMode) {
          return this.rgb(this.r * 1.1, this.g * 2.7, this.b * 2.2)
        } else {
          return this.rgb(this.r, this.g, this.b)
        }
      } else {
        return 'rgb(197,197,197)'
      }
    },
    textColor(): string {
      if (this.$colorMode.value === 'dark') {
        if (this.isWhiteTextMode) {
          return this.rgb(this.r * 1.1, this.g * 2.7, this.b * 2.2)
        } else {
          return this.color
        }
      } else {
        return this.isWhiteTextMode ? 'white' : 'black'
      }
    },
  },
  mounted() {
    this.r = parseInt(this.color.substr(1, 2), 16)
    this.g = parseInt(this.color.substr(3, 2), 16)
    this.b = parseInt(this.color.substr(5, 2), 16)
    this.isWhiteTextMode =
      (this.r * 249 + this.g * 587 + this.b * 134) / 1000 < 172
  },
  methods: {
    getBooleanByColor() {
      // この条件分の閾値を変えれば枠線の付く色の種類を変えれる
      if (this.$colorMode.value === 'dark') {
        return !this.disabled
      } else {
        return this.r + this.g + this.b > 650
      }
    },
    rgb(r: number, g: number, b: number): string {
      return 'rgb(' + r + ',' + g + ',' + b + ')'
    },
  },
})
</script>

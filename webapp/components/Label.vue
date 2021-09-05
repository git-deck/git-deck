<template>
  <span
    :style="{
      border: borderColor,
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
// type DataType = {
//   r: number
//   g: number
//   b: number
//   isWhiteTextMode: boolean
// }
const COLORCODE_MAX = 255
export default Vue.extend({
  name: 'Label',
  props: {
    color: {
      // example : '#rrggbb'
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
  // data(): DataType {
  //   return {
  //     r: 0,
  //     g: 0,
  //     b: 0,
  //     isWhiteTextMode: true,
  //   }
  // },
  computed: {
    r(): number {
      return parseInt(this.color.substr(1, 2), 16)
    },
    g(): number {
      return parseInt(this.color.substr(3, 2), 16)
    },
    b(): number {
      return parseInt(this.color.substr(5, 2), 16)
    },
    isWhiteTextMode(): boolean {
      return (this.r * 249 + this.g * 587 + this.b * 134) / 1000 < 172
    },
    backgroundColor(): string {
      if (this.$colorMode.value === 'dark') {
        return this.rgb(this.r * 0.2, this.g * 0.2, this.b * 0.2)
      } else {
        return this.color
      }
    },
    borderColor(): string {
      let returnVal: string = 'solid 0.2px '
      if (this.$colorMode.value === 'dark') {
        if (this.getBooleanByColorInDarkMode()) {
          returnVal += this.NormalizationInDarkMode(this.r, this.g, this.b)
        } else if (this.getFixedBooleanByColorInDarkMode()) {
          returnVal += this.rgb(this.r * 0.9, this.g * 0.9, this.b * 0.9)
        } else {
          returnVal += this.rgb(this.r * 1.2, this.g * 1.2, this.b * 1.2)
        }
      } else if (this.getBooleanByColorInLightMode()) {
        returnVal += this.NormalizationInLightMode(this.r, this.g, this.b)
      } else {
        returnVal += this.color
      }
      return returnVal
    },
    textColor(): string {
      if (this.$colorMode.value === 'dark') {
        if (this.getBooleanByColorInDarkMode()) {
          return this.NormalizationInDarkMode(this.r, this.g, this.b)
        } else if (this.getFixedBooleanByColorInDarkMode()) {
          return this.rgb(this.r * 0.9, this.g * 0.9, this.b * 0.9)
        } else {
          return this.rgb(this.r * 1.2, this.g * 1.2, this.b * 1.2)
        }
      } else {
        return this.isWhiteTextMode ? 'white' : 'black'
      }
    },
  },

  // mounted() {
  //   this.r = parseInt(this.color.substr(1, 2), 16)
  //   this.g = parseInt(this.color.substr(3, 2), 16)
  //   this.b = parseInt(this.color.substr(5, 2), 16)
  //   this.isWhiteTextMode =
  //     (this.r * 249 + this.g * 587 + this.b * 134) / 1000 < 172
  // },
  methods: {
    getBooleanByColorInLightMode(): boolean {
      // LightModeのときを想定、borderの色を濃くするか否か
      return this.r * -91 + this.g * -287 + this.b * -30 + 100000 < 0
      // rgb(208,255,255), rgb(255,240,255), rgb(255, 255, 112)の3点を通る面を境界としたとき,上の式になる
    },
    getBooleanByColorInDarkMode(): boolean {
      // DarkModeを想定、colorの色を明るくするか
      return this.r * 3 + this.g * 2 + this.b < 500
    },
    getFixedBooleanByColorInDarkMode(): boolean {
      // DarkModeのときを想定、colorが明るいときはTrue
      return this.r * 249 + this.g * 587 + this.b * 134 > 172000
    },
    rgb(r: number, g: number, b: number): string {
      return 'rgb(' + r + ',' + g + ',' + b + ')'
    },
    NormalizationInLightMode(r: number, g: number, b: number): string {
      const BASE = 60 * 3
      if (r === COLORCODE_MAX && g === COLORCODE_MAX && b === COLORCODE_MAX) {
        r = COLORCODE_MAX - 1
        g = COLORCODE_MAX - 1
        b = COLORCODE_MAX - 1
      }
      const MUL = Math.floor(BASE / (r + g + b))
      return this.rgb(
        COLORCODE_MAX - MUL * r,
        COLORCODE_MAX - MUL * g,
        COLORCODE_MAX - MUL * b
      )
    },
    NormalizationInDarkMode(r: number, g: number, b: number): string {
      const BASE = 180 * 3
      if (r === 0 && g === 0 && b === 0) {
        r = 1
        g = 1
        b = 1
      }
      const MUL = Math.floor(BASE / (r + g + b))
      return this.rgb(MUL * r, MUL * g, MUL * b)
    },
  },
})
</script>

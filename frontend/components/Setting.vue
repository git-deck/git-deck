<template>
  <header>
    <span
      >ラベルで絞り込み
      <div id="app">
        <span v-bind:style="style">
          {{ message }}
        </span>
      </div>
    </span>
  </header>
</template>

<script lang="ts">
import Vue from 'vue'
type DataType = {
  style: string
  message: string
}
var color = '#ff0f00'
var message = 'ex_label'
export default Vue.extend({
  data(): DataType {
    return {
      style:
        'font-size:50%;background:' +
        color +
        ';width:20%;text-align:center;border-radius:30px;',

      message: message,
    }
  },
})
</script>

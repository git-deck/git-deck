<template>
  <span v-bind:style="{ background: color }" class="label">
    {{ message }}
  </span>
</template>
<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  name: 'Label',
  props: ['color', 'message'],
})
</script>

<style scoped>
.label {
  font-size: 6px;
  padding: 0px 10px;
  border-radius: 24px;
  display: inline-block;
  vertical-align: middle;
}
</style>
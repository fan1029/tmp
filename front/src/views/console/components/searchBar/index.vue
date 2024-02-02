<script setup lang="ts">
import { ref } from "vue";
import { Search } from "@element-plus/icons-vue";
const input1 = ref("");
</script>

<template>
  <div>
    <el-input
      v-model="input1"
      class="el-input"
      placeholder="资产过滤"
      :suffix-icon="Search"
      style="width: 500px; border-radius: 20px; margin-right: 20px"
    />
  </div>
</template>
<style>
/*搜索input框 */
</style>

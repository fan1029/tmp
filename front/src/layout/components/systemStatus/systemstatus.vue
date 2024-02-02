<script setup lang="ts">
import { ref } from "vue";
import statusMoniter from "@/views/console/components/statusMoniter.vue";
// prop = defineProps(["percentage"]); //tag_id
const percentage = ref(20); //实际的时候修改
</script>

<template>
  <el-text style="margin-right: 10px; font-size: 12px">Task</el-text>
  <el-popover placement="bottom" :width="350" trigger="click">
    <template #reference>
      <div class="demo-progress">
        <el-progress :percentage="percentage" />
      </div>
    </template>
    <statusMoniter />
  </el-popover>
</template>

<style scoped>
.demo-progress .el-progress--line {
  width: 300px;
}
</style>

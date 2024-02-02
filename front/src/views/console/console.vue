<script setup lang="ts">
import { Plus } from "@element-plus/icons-vue";
import { ref, onMounted, onUnmounted } from "vue";
import type { TabPaneName } from "element-plus";
import projectList from "@/views/console/components/projectList.vue";
import mainConsole from "./components/mainConsole.vue";
import opMenu from "@/views/console/components/opMenu/index.vue";
import { startNotifyService } from "@/views/console/components/notifySystem/notify";
const visibilityBinding = ref(false);
const initProjectButton = ref(true);
const openTable = ref(false);
function onImported() {
  visibilityBinding.value = false;
  initProjectButton.value = false;
  openTable.value = true;
}
onMounted(() => {
  startNotifyService();
});
</script>

<template>
  <div>
    <projectList v-model="visibilityBinding" @closeDrawer="onImported" />
    <mainConsole v-if="openTable" />
    <!-- 两个element plus的按钮。一个是新建项目，第二个是导入项目。位于中间居中。-->
    <div style="position: absolute; top: 50%; left: 50%">
      <el-button
        type="primary"
        @click="visibilityBinding = true"
        :icon="Plus"
        :round="true"
        size="large"
        v-if="initProjectButton"
      >
        打开项目控制台</el-button
      >
    </div>
    <opMenu />
  </div>
</template>
<style scoped>
.demo-tabs > .el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}

.max-height-row {
  max-height: 10px; /* 设置最大行高度为60px，根据你的需求调整 */
  overflow: hidden; /* 如果内容溢出，隐藏溢出部分 */
}
.el-tooltip__popper {
  font-size: 14px;
  max-width: 50%;
  max-height: 50%;
}
</style>

<script setup lang="ts">
import { ref } from "vue";
import consoleTable from "@/views/console/components/consoleTable.vue";
import { useTagStore } from "@/store/modules/tag";
import { storeToRefs } from "pinia";

import { onMounted } from "vue";

const tagStore = useTagStore();
const openPluginName = ref("");
//设置projectId
// tagStore.setProjectId(10);

const tagInfoList = ref([]);
tagInfoList.value = tagStore.getTagInfoList();

onMounted(() => {
  console.log(1);
  console.log(tagInfoList.value);
});
</script>
<template>
  <div>
    <el-row :gutter="10">
      <el-col :span="24">
        <el-card style="border-radius: 12px; padding: 15px" class="infoCard">
          <div class="mainConsole">
            <el-tabs
              tab-position="right"
              style="height: 100%"
              class="tableTabs"
            >
              <el-tab-pane
                v-for="tagInfo in tagInfoList"
                :label="tagInfo.name"
                :key="tagInfo.id"
                ><consoleTable :tag_id="tagInfo.id"
              /></el-tab-pane>
            </el-tabs>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>
<style lang="scss">
.tableTabs {
  /* 右侧往右移动200px */
  position: relative;
}
.el-tabs__item {
  margin-left: -10px;
  max-width: 70px; /* 你想要的最大宽度 */
}

.infoCard {
  border-radius: 20px;
  height: 100%;
  /* 阴影 */
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}
</style>

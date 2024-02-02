<script setup lang="ts">
defineOptions({
  name: "404"
});
import { ref } from "vue";
import type { TabPaneName } from "element-plus";
import projectList from "@/views/error/components/projectList.vue";
import { getProjectInfo } from "@/api/project";
import superTable from "@/views/console/components/superTable.vue";

const drawer2 = ref(false);
const editableTabsValue = ref("2");
const editableTabs = ref([
  {
    title: "Tab 1",
    name: "1",
    content: "Tab 1 content"
  }
]);

const handleTabsEdit = (
  targetName: TabPaneName | undefined,
  action: "remove" | "add"
) => {
  if (action === "add") {
    drawer2.value = true;
    // const newTabName = `${++tabIndex}`;
    // table.value = true;
    // editableTabs.value.push({
    //   title: "New Tab",
    //   name: newTabName,
    //   content: "New Tab content"
    // });
    // editableTabsValue.value = newTabName;
  } else if (action === "remove") {
    const tabs = editableTabs.value;
    let activeName = editableTabsValue.value;
    if (activeName === targetName) {
      tabs.forEach((tab, index) => {
        if (tab.name === targetName) {
          const nextTab = tabs[index + 1] || tabs[index - 1];
          if (nextTab) {
            activeName = nextTab.name;
          }
        }
      });
    }

    editableTabsValue.value = activeName;
    editableTabs.value = tabs.filter(tab => tab.name !== targetName);
  }
};

async function getProjectListData(projectId) {
  // 循环遍历projectId数组取出id字段
  for (let i = 0; i < projectId.value.length; i++) {
    console.log(projectId.value[i].id);
    //调用getProjectInfo请求数据带入id
    const res = await getProjectInfo(projectId.value[i].id);
    console.log(res);
    drawer2.value = false;
  }
}
</script>

<template>
  <div style="margin-bottom: 20px">
    <projectList v-model="drawer2" @submitProjectIds="getProjectListData" />
    <el-tabs
      v-model="editableTabsValue"
      class="demo-tabs"
      editable
      @edit="handleTabsEdit"
    >
      <el-tab-pane
        v-for="item in editableTabs"
        :key="item.name"
        :label="item.title"
        :name="item.name"
      >
        <el-row class="mb-4">
          <el-button type="primary">待定</el-button>
          <el-button type="success">待定</el-button>
          <el-button type="info">待定</el-button>
          <el-button type="warning">待定</el-button>
          <el-button type="danger">待定</el-button>
        </el-row>

        <superTable />
      </el-tab-pane>
    </el-tabs>
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

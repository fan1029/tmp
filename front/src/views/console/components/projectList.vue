<script setup lang="ts">
import {
  getProjectList,
  createProject,
  ProjectCreateRequest
} from "@/api/project";
import { ref, provide } from "vue";
import { ElMessage } from "element-plus";
import { useTagStoreHook } from "@/store/modules/tag";
// const visibilityBinding = ref(false);
const currentProjectId = ref(-1);
const newProjectName = ref("");
const newProjectDescription = ref("");
const newProjectAsset = ref("");
const projectList = ref([]);
const loading = ref(true);
const submitAssetButtonStatus = ref(false);
const emit = defineEmits(["submitProjectIds", "closeDrawer"]);
const tagStore = useTagStoreHook();
//Promise例子
function getProjectListData() {
  return new Promise(() => {
    //请求getProjectList成功则将数据赋值给projectList
    getProjectList()
      .then(res => {
        if (res.status == 200) {
          projectList.value = res.data;
        }
      })
      .then(() => {
        loading.value = false;
      });
  });
}

const currentRow = ref();

function handleCurrentChange(val) {
  currentRow.value = val;
  console.log(currentRow.value);
}
const submitProjectIds = () => {
  tagStore.setProjectId(currentRow.value.id);
  tagStore.getTagInfoQuery().then(() => {
    loading.value = true;
    emit("closeDrawer");
  });
};

function handleTabClick(tab) {
  if (tab.props.label == "历史") {
    console.log("历史");
    getProjectListData();
  } else if (tab.props.label == "新建") {
    console.log("新建");
    loading.value = true;
  }
}
// 提交资产逻辑
function submitAsset() {
  submitAssetButtonStatus.value = true;
  console.log(newProjectAsset.value);
  const assetList = newProjectAsset.value.split("\n");
  newProjectAsset.value = "";
  console.log(assetList);
  const projectCreateRequest: ProjectCreateRequest = {
    name: newProjectName.value,
    description: newProjectDescription.value,
    assets: assetList,
    createUser: "admin"
  };
  createProject(projectCreateRequest)
    .then(res => {
      console.log(res);
      tagStore.setProjectId(res.project_id);
      tagStore.getTagInfoQuery().then(() => {
        emit("closeDrawer");
      });
      submitAssetButtonStatus.value = false;
      ElMessage({
        message: res.msg,
        type: res.status ? "success" : "error"
      });
      newProjectName.value = "";
      newProjectDescription.value = "";
    })
    .catch(() => {
      submitAssetButtonStatus.value = false;
    });
}
</script>

<template>
  <!-- <el-button type="primary">Open Drawer</el-button> -->
  <el-drawer
    title="添加项目"
    :modal-append-to-body="true"
    direction="rtl"
    size="40%"
  >
    <el-tabs
      tab-position="left"
      style="height: 70%"
      class="demo-tabs"
      @tab-click="handleTabClick"
    >
      <el-tab-pane label="新建">
        <el-form label-width="80px" class="forms1">
          <el-form-item label="项目名">
            <el-input v-model="newProjectName" placeholder="请输入项目名" />
          </el-form-item>
          <el-form-item label="描述">
            <el-input
              v-model="newProjectDescription"
              placeholder="请输入描述"
            />
          </el-form-item>
          <el-form-item label="资产">
            <el-input
              v-model="newProjectAsset"
              type="textarea"
              placeholder="一行一个"
              max-height="50px"
              resize="none"
            />
          </el-form-item>
          <el-form-item>
            <el-button
              type="primary"
              @click="submitAsset"
              :disabled="submitAssetButtonStatus"
              >提交</el-button
            >
          </el-form-item>
        </el-form>
      </el-tab-pane>
      <el-tab-pane name="hs" label="历史"
        ><el-table
          v-loading="loading"
          :data="projectList"
          row-key="id"
          class="projectListTable"
          max-height="300px"
          highlight-current-row
          table-layout="auto"
          @current-change="handleCurrentChange"
        >
          <el-table-column property="id" label="Id" v-if="false" />
          <el-table-column property="name" label="项目名" />
          <el-table-column property="description" label="描述" />
          <el-table-column property="create_time" label="创建时间" />
          <el-table-column property="source" label="来源" v-if="false" />
        </el-table>
        <el-button type="primary" @click="submitProjectIds" class="appendButton"
          >添加到数据台</el-button
        >
      </el-tab-pane>
    </el-tabs>
  </el-drawer>
</template>

<style scoped>
.projectListTable {
  margin-left: 10px;
}
/* 将class为demo-tabs的el-tabs元素左移，使其与el-drawer元素重合 */
.demo-tabs {
  margin-left: -20px;
}
.forms1 {
  margin-left: -20px;
}
.appendButton {
  margin-top: 30px;
  margin-left: 20px;
}
</style>

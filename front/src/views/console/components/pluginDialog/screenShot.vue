<script setup lang="ts">
import { ref, watch, defineProps } from "vue";
import { runPluginApi, getPluginInfoApi } from "@/api/service";
import { ElMessage } from "element-plus";
const pluginName = "Plugin_screenShot";
const p = defineProps(["openInfo"]);
const gobyopenStatus = ref(false);
const currentTarget = ref({ id: -1, asset_name: "" });
const region = ref("asset_selected");
watch(
  () => {
    try {
      return p.openInfo.pluginName;
    } catch (error) {
      return "";
    }
  },
  val => {
    if (val == pluginName) {
      gobyopenStatus.value = true;
      currentTarget.value.id = p.openInfo.assetId;
      currentTarget.value.asset_name = p.openInfo.assetName;
      getPluginInfoApi({ pluginName: "Plugin_screenShot" }).then(res => {
        pluginInfo.value = res.data;
      });
    }
  }
);
const pluginInfo = ref({});
function runPlugin() {
  let assetId = -1;
  if (region.value == "asset_selected") {
    assetId = currentTarget.value.id;
  } else {
    assetId = -2;
  }
  const scanConfig = {};
  runPluginApi({
    tagId: p.openInfo.tag_id,
    pluginName: pluginName,
    assetId: assetId,
    config: scanConfig
  }).then(res => {
    ElMessage.success(res.msg);
    gobyopenStatus.value = false;
  });
}
</script>
<template>
  <div>
    <el-dialog
      v-model="gobyopenStatus"
      :title="pluginInfo.pluginName"
      width="40%"
      align-center
      style="border-radius: 12px"
    >
      <el-descriptions
        class="margin-top"
        title="插件信息"
        :column="2"
        size="small"
        border
      >
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">插件名</div>
          </template>
          {{ pluginInfo.pluginName }}
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">目标</div>
          </template>
          <el-tag
            v-for="item in pluginInfo.scanTargetType"
            :key="item"
            style="margin-right: 5px"
          >
            {{ item }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">涉及列</div>
          </template>
          <!-- span v-for 遍历pluginInfo.columnDict -->
          <el-tag
            v-for="(value, key) in pluginInfo.columnDict"
            :key="key"
            style="margin-right: 10px"
          >
            {{ value }}:{{ key }}</el-tag
          >
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">版本</div>
          </template>
          <span size="small">{{ pluginInfo.version }}</span>
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">简介</div>
          </template>
          <span size="small">{{ pluginInfo.description }}</span>
        </el-descriptions-item>
      </el-descriptions>
      <el-descriptions
        class="margin-top"
        title="扫描配置"
        :column="2"
        size="small"
        style="margin-top: 15px"
        border
      />
      <el-form>
        <el-form-item label="扫描目标">
          <el-select v-model="region" placeholder="please select">
            <el-option
              :label="currentTarget.asset_name"
              value="asset_selected"
            />
            <el-option label="所有资产" value="asset_all" />
          </el-select>
        </el-form-item>
        <el-button
          type="primary"
          @click="runPlugin"
          round
          style="margin-left: 90%"
          >开始</el-button
        >
      </el-form>
    </el-dialog>
  </div>
</template>
<style scoped>
.slider-demo-block {
  display: flex;
  align-items: center;
}
.slider-demo-block .el-slider {
  margin-top: 0;
  margin-left: 12px;
}
.slider-demo-block .demonstration {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  line-height: 44px;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-bottom: 0;
}
.slider-demo-block .demonstration + .el-slider {
  flex: 0 0 70%;
}
</style>

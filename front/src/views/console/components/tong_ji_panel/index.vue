<script setup lang="ts">
import { ref } from "vue";
import { useMenuStatusStore } from "@/store/modules/menuSatus";
import { storeToRefs } from "pinia";
const infoStore = useMenuStatusStore();
const { systemInfo, taskInfo } = storeToRefs(infoStore);
</script>
<template>
  <div>
    <div style="margin-top: -20px">
      <el-row :gutter="5">
        <el-col :span="8">
          <div class="statistic-card">
            <el-statistic :value="taskInfo.allAsset">
              <template #title>
                <div style="display: inline-flex; align-items: center">
                  总资产
                  <el-tooltip
                    effect="dark"
                    content="Number of users who logged into the product in one day"
                    placement="top"
                  >
                    <el-icon style="margin-left: 4px" :size="12">
                      <Warning />
                    </el-icon>
                  </el-tooltip>
                </div>
              </template>
            </el-statistic>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="statistic-card">
            <el-statistic :value="taskInfo.allTaskCount">
              <template #title>
                <div style="display: inline-flex; align-items: center">
                  任务数
                  <el-tooltip
                    effect="dark"
                    content="Number of users who logged into the product in one month"
                    placement="top"
                  >
                    <el-icon style="margin-left: 4px" :size="12">
                      <Warning />
                    </el-icon>
                  </el-tooltip>
                </div>
              </template>
            </el-statistic>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="statistic-card">
            <el-statistic
              :value="taskInfo.runningTaskCount"
              title="New transactions today"
            >
              <template #title>
                <div style="display: inline-flex; align-items: center">
                  运行中
                </div>
              </template>
            </el-statistic>
          </div>
        </el-col>
      </el-row>
    </div>
    <div>
      <el-progress
        type="dashboard"
        :percentage="0"
        :width="80"
        status="success"
      >
        <template #default="{ percentage }">
          <span class="percentage-value">{{ percentage }}%</span>
          <span class="percentage-label">Tasks</span>
        </template>
      </el-progress>
      <el-progress
        type="dashboard"
        :percentage="systemInfo.cpu"
        :width="80"
        status="warning"
      >
        <template #default="{ percentage }">
          <span class="percentage-value">{{ percentage }}%</span>
          <span class="percentage-label">CPU</span>
        </template>
      </el-progress>
      <el-progress type="dashboard" :percentage="systemInfo.mem" :width="80">
        <template #default="{ percentage }">
          <span class="percentage-value">{{ systemInfo.mem }}%</span>
          <span class="percentage-label">Menory</span>
        </template>
      </el-progress>
    </div>
  </div>
</template>

<style scoped>
:global(h2#card-usage ~ .example .example-showcase) {
  background-color: var(--el-fill-color) !important;
}

.el-statistic {
  --el-statistic-content-font-size: 28px;
}

.statistic-card {
  height: 100%;
  padding: 20px;
  border-radius: 4px;
  background-color: var(--el-bg-color-overlay);
}

.statistic-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  font-size: 12px;
  color: var(--el-text-color-regular);
  margin-top: 16px;
}

.statistic-footer .footer-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.statistic-footer .footer-item span:last-child {
  display: inline-flex;
  align-items: center;
  margin-left: 4px;
}

.green {
  color: var(--el-color-success);
}
.red {
  color: var(--el-color-error);
}
.percentage-value {
  display: block;
  margin-top: 10px;
  font-size: 28px;
}
.percentage-label {
  display: block;
  margin-top: 10px;
  font-size: 12px;
}
.demo-progress .el-progress--line {
  margin-bottom: 15px;
  width: 350px;
}
.demo-progress .el-progress--circle {
  margin-right: 15px;
}

.el-progress {
  margin-left: 10px;
  margin-right: 10px;
}

.percentage-value {
  cursor: pointer;
  margin-top: 10px;
  font-size: 20px;
}
</style>

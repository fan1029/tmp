<script setup lang="ts">
import { ref } from "vue";
import { SwitchButton, Tools } from "@element-plus/icons-vue";
import statusMoniter from "@/views/console/components/statusMoniter.vue";
import operateLog from "@/views/console/components/operateLog/index.vue";
import userInfoCard from "@/views/console/components/userInfoCard/index.vue";
const activeNames = ref(["1"]);
const handleChange = (val: string[]) => {
  console.log(val);
};
const a = ref(false);
const testData = [
  { consumer_name: "Goby-1123123123", status: "close" },
  { consumer_name: "Goby-2", status: "running" },
  { consumer_name: "Goby-3", status: "close" },
  { consumer_name: "截图-1", status: "close" }
];
</script>
<template>
  <div>
    <div class="demo-collapse">
      <el-collapse v-model="activeNames" @change="handleChange">
        <el-collapse-item title="操作" name="1">
          <div>
            <el-scrollbar>
              <el-button type="primary" round>刷新</el-button>
              <el-button type="primary" round>导出</el-button>
              <el-button type="primary" round>任务队列</el-button>
            </el-scrollbar>
          </div>
        </el-collapse-item>
      </el-collapse>
      <el-collapse>
        <el-collapse-item title="运行状态" name="21">
          <statusMoniter />
        </el-collapse-item>
      </el-collapse>
      <el-collapse>
        <el-collapse-item title="资产统计" name="21">
          <div>
            Consistent with real life: in line with the process and logic of
            real life, and comply with languages and habits that the users are
            used to;
          </div>
        </el-collapse-item>
      </el-collapse>

      <el-collapse>
        <el-collapse-item title="操作记录" name="21">
          <div style="margin-left: 8px"><operateLog /></div>
        </el-collapse-item>
      </el-collapse>
      <el-collapse>
        <el-collapse-item title="插件1" name="21">
          <div>
            Consistent with real life: in line with the process and logic of
            real life, and comply with languages and habits that the users are
            used to;
          </div>
        </el-collapse-item>
      </el-collapse>
    </div>
  </div>
</template>
<style scoped>
.status_card {
  height: 10px;
  max-height: 440px;
  width: 240px;
  border-radius: 10px;
  background-color: rgba(205, 229, 250, 0.568);
}
.el-collapse-item__wrap {
  transition: height 0.3s ease; /* 这里的0.3s和ease可以根据需要进行调整 */
}
</style>

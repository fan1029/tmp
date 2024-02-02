<script setup lang="ts">
import { ref, onMounted } from "vue";
import { changeServiceStatusApi } from "@/api/service";
import { SwitchButton, Tools } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
import { useMenuStatusStore } from "@/store/modules/menuSatus";
import { storeToRefs } from "pinia";
import { store } from "@/store";
// const props = defineProps(["statusData"]); //tag_id
// const loadStatusFlg = ref(false);
type consumerStatusType = {
  consumer_name: string;
  status: string;
  maxThread: number;
  runningThreadCount: number;
  mode: number;
  heartBetTime: number;
};
const infoStore = useMenuStatusStore();
const { serviceStatus } = storeToRefs(infoStore);

const centerDialogVisible = ref(false);
const currentSelectedConsumer = ref("");
const currentSelectedConsumerStatus = ref({} as consumerStatusType);
function getConsumerStatus(consumer_name: string) {
  //遍历consumerStatusData.value，找到对应的consumer_name
  for (let i = 0; i < serviceStatus.value.length; i++) {
    if (serviceStatus.value[i].consumer_name == consumer_name) {
      currentSelectedConsumerStatus.value = serviceStatus.value[i];
      console.log(currentSelectedConsumerStatus.value);
      break;
    }
  }
}

function changeServiceStatus(consumer_name: string) {
  console.log("switchConsumerStatus");
  getConsumerStatus(consumer_name);
  const maxThread = currentSelectedConsumerStatus.value.maxThread;
  const status = currentSelectedConsumerStatus.value.status;
  if (status != "close") {
    currentSelectedConsumerStatus.value.status = "shutDown";
  } else {
    currentSelectedConsumerStatus.value.status = "open";
  }
  console.log(maxThread);
  console.log(status);
  changeServiceStatusApi({
    consumerName: consumer_name,
    maxThread: maxThread,
    status: currentSelectedConsumerStatus.value.status
  })
    .then(res => {
      ElMessage({
        message: "修改成功",
        type: "success"
      });
      console.log(res);
    })
    .catch(err => {
      console.log(err);
    });
}

function getConsuerInfo(consumer_name) {
  console.log(consumer_name);
  currentSelectedConsumer.value = consumer_name;
  console.log(currentSelectedConsumer.value);
  getConsumerStatus(consumer_name);
  console.log(currentSelectedConsumerStatus.value);
  centerDialogVisible.value = true;
}
</script>

<template>
  <div>
    <div>
      <el-table :data="serviceStatus">
        <el-table-column
          width="250px"
          label="消费者"
          prop="consumer_name"
          show-overflow-tooltip
        />
        <el-table-column label="状态" prop="status" />
        <el-table-column label="操作">
          <template #default="scope">
            <el-icon
              ><SwitchButton
                @click="changeServiceStatus(scope.row.consumer_name)"
                style="color: red"
            /></el-icon>
            <el-icon
              @click="getConsuerInfo(scope.row.consumer_name)"
              style="margin-left: 10px"
              ><Tools
            /></el-icon>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div>
      <el-dialog
        v-model="centerDialogVisible"
        title="消费者详细"
        width="35%"
        align-center
        append-to-body
      >
        <div style="margin-left: 130px">
          <!-- 表单选择数字，设置运行数量，只允许选择数字 -->
          <el-form>
            <el-form-item label="hostName:">
              <el-text tag="b">{{
                currentSelectedConsumerStatus.hostName
              }}</el-text>
            </el-form-item>
            <el-form-item label="consumer_identification:">
              <el-text tag="b">{{
                currentSelectedConsumerStatus.consumer_identification
              }}</el-text>
            </el-form-item>
            <el-form-item label="runningThreadCount:">
              <el-text tag="b">{{
                currentSelectedConsumerStatus.runningThreadCount
              }}</el-text>
            </el-form-item>
            <el-form-item label="maxThread:">
              <el-input-number
                v-model="currentSelectedConsumerStatus.maxThread"
                :min="1"
                :max="10"
              />
            </el-form-item>
            <el-form-item label="heartBeatTime:">
              <el-text tag="b">{{
                currentSelectedConsumerStatus.heartBeatTime
              }}</el-text>
            </el-form-item>
          </el-form>
        </div>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="centerDialogVisible = false">Cancel</el-button>
            <el-button type="primary" @click="centerDialogVisible = false">
              Confirm
            </el-button>
          </span>
        </template>
      </el-dialog>
    </div>
  </div>
</template>

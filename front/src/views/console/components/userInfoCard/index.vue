<script setup lang="ts">
import { ref } from "vue";
import { User } from "@element-plus/icons-vue";
const onlineUserList = [
  {
    id: 1,
    username: "maple",
    intrduction: "XX公司"
  },
  {
    id: 2,
    username: "user2",
    intrduction: "XX公司"
  },
  {
    id: 3,
    username: "guest",
    intrduction: "XX公司"
  }
];
</script>
<template>
  <div>
    <el-scrollbar max-height="150px">
      <el-card
        :key="index"
        v-for="(item, index) in onlineUserList"
        style="
          margin-left: 3px;
          height: 70px;
          width: 210px;
          border-radius: 12px;
          margin-bottom: 2px;
        "
      >
        <el-row :gutter="2">
          <el-col :span="8">
            <el-avatar
              src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"
              style="margin-top: 10px; margin-left: 5px"
            />
          </el-col>
          <el-col :span="16">
            <div>
              <el-text class="userinfocard" style="margin-top: -8px"
                >用户名: {{ item.username }}</el-text
              >
            </div>
            <div>
              <el-text class="userinfocard2" style="margin-top: 3px">{{
                item.intrduction
              }}</el-text>
            </div>
          </el-col>
        </el-row>
      </el-card>
    </el-scrollbar>
  </div>
</template>
<style scoped></style>

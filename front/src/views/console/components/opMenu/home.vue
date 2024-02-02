<script setup lang="ts">
import { ref } from "vue";
import operateLogPage from "@/views/console/components/operateLog/index.vue";
import statuMoniter from "@/views/console/components/statusMoniter.vue";
import OnlineUser from "@/views/console/components/userInfoCard/index.vue";
import TongjiPanel from "@/views/console/components/tong_ji_panel/index.vue";




</script>
<template>
  <div>
    <el-row>
      <el-col :span="7">
        <el-card
          shadow="hover"
          style="
            height: 540px;
            width: 250px;
            border-radius: 15px;
            padding: 15px;
            padding-top: 20px;
          "
        >
          <el-scrollbar height="570px"
            ><operateLogPage style=""
          /></el-scrollbar> </el-card
      ></el-col>
      <el-col :span="12">
        <div>
          <el-row :gutter="100">
            <el-col :span="12">
              <el-card
                shadow="hover"
                style="
                  height: 200px;
                  width: 250px;
                  border-radius: 15px;
                  padding: 15px;
                  padding-top: 20px;
                "
                ><OnlineUser
              /></el-card>
            </el-col>
            <el-col :span="12">
              <el-card
                shadow="hover"
                style="
                  height: 200px;
                  width: 350px;
                  border-radius: 15px;
                  padding: 15px;
                  padding-top: 20px;
                "
                ><TongjiPanel
              /></el-card>
            </el-col>
          </el-row>
          <el-card
            shadow="hover"
            style="
              height: 300px;
              width: 630px;
              border-radius: 15px;
              padding: 15px;
              padding-top: 20px;
              margin-top: 40px;
            "
            ><statuMoniter
          /></el-card>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

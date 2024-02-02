<template>
  <div>
    <el-container>
      <el-aside width="55px">
        <el-menu
          default-active="home"
          class="el-menu-vertical-demo"
          :collapse="true"
          style="height: 600px; padding-left: 13px; padding-top: 10px"
          @select="handleOpen"
        >
          <el-menu-item index="home">
            <el-icon><House /></el-icon>
            <template #title>主页</template>
          </el-menu-item>
          <el-menu-item index="tmp">
            <el-icon><icon-menu /></el-icon>
            <template #title>Two</template>
          </el-menu-item>
        </el-menu></el-aside
      >
      <el-main
        ><div id="submenu-s">
          <component :is="pageReg[currentKey]" />
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import {
  Document,
  Menu as IconMenu,
  Location,
  House,
  Setting
} from "@element-plus/icons-vue";
import HomePage from "./home.vue";
const pageReg = { home: HomePage };
const currentKey = ref("home");
function handleOpen(key: string, keyPath: string) {
  console.log(key, keyPath);
  currentKey.value = key;
}
</script>

<style scoped>
.el-main {
  --el-main-padding: 0px;
}
.el-aside {
  overflow: hidden;
}
#submenu-s {
  height: 600px;
  width: 945px;
  background-color: #f2f3f5;
  padding-left: 20px;
  padding-top: 20px;
}
</style>

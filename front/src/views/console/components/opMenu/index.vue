<script setup lang="ts">
import { Menu } from "@element-plus/icons-vue";
import menupage from "@/views/console/components/opMenu/menu.vue";
import { useMenuStatusStore } from "@/store/modules/menuSatus";
import { useTagStore } from "@/store/modules/tag";
import { ref, onMounted, onUnmounted } from "vue";
import { storeToRefs } from "pinia";
import { store } from "@/store";
import { getConfig } from "@/config";

const wsServer = "ws://" + getConfig().serverHost + "/service/menuIndexInfo";
const menuVisibility = ref(false);

const { project_id } = storeToRefs(useTagStore(store));
const socket = new WebSocket(wsServer);
socket.onmessage = function (event) {
  const infoStore = useMenuStatusStore(store);
  infoStore.setInfoData(JSON.parse(event.data));
};
function syncIndexInfo() {
  if (socket.readyState != 1) {
    return;
  }
  socket.send(
    JSON.stringify({ command: "getSystemInfo", projectId: project_id.value })
  );
  socket.send(
    JSON.stringify({ command: "getTaskCount", projectId: project_id.value })
  );
  socket.send(
    JSON.stringify({ command: "getServiceStatus", projectId: project_id.value })
  );
}

onMounted(() => {
  syncIndexInfo();
  setInterval(() => {
    syncIndexInfo();
  }, 1000);
});

onUnmounted(() => {
  socket.close();
});
</script>
<template>
  <div>
    <div>
      <el-button
        @click="menuVisibility = !menuVisibility"
        class="menu-button"
        circle
        :icon="Menu"
        size="large"
      />
    </div>
    <div v-if="menuVisibility" class="menupos">
      <el-card style="border-radius: 15px">
        <menupage />
      </el-card>
    </div>
  </div>
</template>
<style>
.el-card__body {
  padding: 0px !important;
}

.menu-button {
  position: fixed; /* 固定定位 */
  bottom: 11px; /* 底部对齐 */
  left: 50%; /* 左边距离50% */
  transform: translateX(-50%); /* 向左移动元素宽度的50% */
  z-index: 9999;
}

.menupos {
  position: fixed; /* 固定定位 */
  bottom: 3%;
  left: 50%; /* 左边距离50% */
  transform: translateX(-50%); /* 向左移动元素宽度的50% */
  z-index: 1009;
}
.menu-button {
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}

.menu-button:hover {
  filter: drop-shadow(0em 0em 1.3em #79bbff);
}

.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  min-height: 400px;
}

#submenu-main {
  height: 600px;
  width: 945px;
  background-color: #e7e7e7;
  padding-left: 20px;
  padding-top: 10px;
  /* 添加投影 */
  box-shadow: 0 0 10px rgb(0, 0, 0);
}
</style>

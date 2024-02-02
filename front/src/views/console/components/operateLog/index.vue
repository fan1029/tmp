<script setup lang="ts">
import { ref } from "vue";

const activities = [
  {
    content: "maple添加资产:www.baidu.com",
    timestamp: "2018-04-12 20:47",

    type: "primary"
  },
  {
    content: "maple删除资产:www.baidu.com",
    timestamp: "2018-04-03 20:46",
    color: "#0bbd87"
  },
  {
    content: "maple添加笔记:www.baidu.com",
    timestamp: "2018-04-03 20:46"
  },
  {
    content: "maple:www.baidu.com->goby插件",
    timestamp: "2018-04-03 20:46",
    type: "primary",
    hollow: true
  },
  {
    content: "maple上线",
    timestamp: "2018-04-03 20:46"
  }
];
</script>
<template>
  <div>
    <el-timeline>
      <el-timeline-item
        v-for="(activity, index) in activities"
        :key="index"
        :color="activity.color"
        :hollow="activity.hollow"
        :timestamp="activity.timestamp"
      >
        {{ activity.content }}
      </el-timeline-item>
    </el-timeline>
  </div>
</template>

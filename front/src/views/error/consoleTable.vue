<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useTagStoreHook } from "@/store/modules/tag";
import { storeToRefs } from "pinia";
import { Tag } from "@/store/modules/tag";
//接受父组件传来的tag_id参数

const props = defineProps(["tag_id"]);
const tagStore = useTagStoreHook(); //pinia
const tag = storeToRefs(tagStore.getTagById(props.tag_id)); //根据tag_id获取tag
// const originalData = ref([]);
const columnInfo = ref({});
const currentProjectId = ref(-1);
const currentTagId = ref(-1);
const currentColumn = ref([]);
const pageSize = ref(10); //每页显示多少条
const currentPage = ref(1); //当前页
const sort = ref("asc"); //排序方式
const sortColumn = ref("asset_original"); //排序字段

// onMounted(() => {
//   tagStore.getAssetDataQuery();
// });
</script>
<template>
  <div>
    <el-table max-height="700px" style="border-radius: 20px">
      <el-table-column fixed type="expand" />
      <el-table-column
        v-for="(column, index) in tag.data.column"
        :key="index"
        :property="column.name"
        :label="column.label"
        :sortable="column.sort ? true : false"
    /></el-table>
  </div>
</template>

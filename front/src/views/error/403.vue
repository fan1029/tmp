<script lang="ts" setup>
import { useTagStoreHook, Tag, Asset } from "@/store/modules/tag";
// 定义测试数据
import { onMounted } from "vue";
const tagStore = useTagStoreHook();
// 写一个Asset类型的测试数据
const tasset: Asset = {
  asset_original: "www.baidu.com",
  columns: [
    { name: 123123, a: "123123" },
    { name: "asdasd", c: "cccc" }
  ]
};
const tasset2: Asset = {
  asset_original: "www.baidu1.com",
  columns: [
    { name: 123123, a: "123123" },
    { name: "asdasd", c: "cccc" }
  ]
};
const tasset3: Asset = {
  asset_original: "www.1baidu1.com",
  columns: [
    { name: 123123, a: "123123" },
    { name: "asdasd", c: "cccc" }
  ]
};
//写Tag类型的测试数据
const tTag: Tag = {
  name: "1232123",
  assetMap: new Map<string, Asset>([["www.baidu.com", tasset]])
};
const tTag2: Tag = {
  name: "ac",
  assetMap: new Map<string, Asset>([["www.baidu1.com", tasset2]])
};

// onMounted(() => {
//   tagStore.setTagMap(
//     new Map<string, Tag>([
//       ["123123", tTag],
//       ["123121231231231233", tTag]
//     ])
//   );
// });

// 创建tag测试
async function ceshi1() {
  const res = await tagStore.getAssetDataQuery(
    10,
    12,
    10,
    1,
    "asc",
    "asset_original"
  );
  console.log(res);
}

function createTagCeshi() {
  tagStore.addTag("12");
}

onMounted(() => {
  createTagCeshi();
});

// 获取所有标签并在Store中放入，测试用
// async function ceshi1() {
//   const res = await tagStore.getProjectTag(1);
//   console.log(res);
// }
</script>

<template>
  <div>
    <a @click="ceshi1">123123123123</a>
  </div>
</template>

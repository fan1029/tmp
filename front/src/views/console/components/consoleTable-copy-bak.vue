<script setup lang="ts">
import { ref, nextTick, computed, onMounted } from "vue";
import { useTagStoreHook } from "@/store/modules/tag";
import { CustomMouseMenu } from "@howdyjs/mouse-menu";
import { message } from "@/utils/message";
import { Link, ChatDotSquare } from "@element-plus/icons-vue";
import dialogCenter from "@/views/console/components/pluginDialog/index.vue";
import tableToolBar from "@/views/console/components/tableToolBar/index.vue";
import { useWebSocket } from "vue-native-websocket";

//接受父组件传来的tag_id参数
// 表格数据代码
const maxCellHeight = "100px"; //单元格最大高度
const props = defineProps(["tag_id"]); //tag_id
const tagStore = useTagStoreHook(); //pinia
const ready = ref(false);
const openPluginInfo = ref({ pluginName: "", assetName: "", assetId: -1 });
let columnInfo;
let rows;
let total;

// #####################################   websocket重写 ##########################
const socket = useWebSocket("ws://127.0.0.1:5000/tag/syncTable");
onMounted(() => {
  socket.value.onopen = function () {
    // console.log("表格同步服务连接成功");
    message("表格同步服务连接成功", {
      type: "success"
    });
  };
  socket.value.onmessage = function (event) {
    console.log(event.data);
    if (event.data == "update") {
      console.log("update");
      getAssetData();
    }
  };
});

getAssetData()
  .then(() => {
    columnInfo = computed(() => tagStore.getColumn(props.tag_id));
    rows = computed(() => tagStore.getRows(props.tag_id));
    total = computed(() => tagStore.tagMap.get(props.tag_id.toString()).total);
  })
  .then(() => {
    ready.value = true;
  });
async function getAssetData() {
  await tagStore.getAssetDataQuery(props.tag_id);
}

const pageSize = ref(10); //每页显示多少条
const currentPage = ref(1); //当前页
const sort = ref("asc"); //排序方式
const sortColumn = ref("asset_original"); //排序字段
const tableLoadingStatus = ref(false); //表格加载状态
//总条数
// console.log(total);

function handleSizeChange(val: number) {
  pageSize.value = val;
  tableLoadingStatus.value = true;
  tagStore
    .getAssetDataQuery(props.tag_id, pageSize.value, currentPage.value)
    .then(() => {
      tableLoadingStatus.value = false;
    })
    .catch(() => {
      tableLoadingStatus.value = false;
    });
}
function handleCurrentChange(val: number) {
  currentPage.value = val;
  tagStore
    .getAssetDataQuery(props.tag_id, pageSize.value, currentPage.value)
    .then(() => {
      tableLoadingStatus.value = false;
    })
    .catch(() => {
      tableLoadingStatus.value = false;
    });
}

function openNewWindow(url: string) {
  window.open(url, "_blank");
}

// 表格数据代码结束

// 菜单代码开始
const menuOptions = {
  menuList: [
    {
      label: ({ row }) => `${row.asset_name}`,
      disabled: true
    },
    {
      label: "详细",
      tips: "Detail",
      fn: row => {
        message(`您查看了第${row.rowIndex}行，数据为`, {
          type: "success"
        });
        console.log(row.rowIndex);
        console.log(row.row);
        console.log(row.row.asset_name);
        console.log(row.row.original_asset);
      }
    },
    {
      label: "编辑",
      tips: "Edit",
      fn: row =>
        message(`您编辑了第${row.rowIndex}行，数据为`, {
          type: "success"
        })
    },
    {
      label: "删除",
      tips: "Delete",
      fn: row =>
        message(`您删除了第${row.rowIndex}行，数据为`, {
          type: "success"
        })
    },
    {
      label: "标注",
      tips: "Tag",
      children: [
        {
          label: "红",
          tips: "red",
          fn: row =>
            message(`您插件了第${row.rowIndex}行，数据为`, {
              type: "success"
            })
        },
        {
          label: "蓝",
          tips: "blue",
          fn: row =>
            message(`您插件了第${row.rowIndex}行，数据为`, {
              type: "success"
            })
        },
        {
          label: "绿",
          tips: "green",
          fn: row =>
            message(`您插件了第${row.rowIndex}行，数据为`, {
              type: "success"
            })
        }
      ]
    },

    {
      label: "插件",
      tips: "Plugin",
      children: [
        {
          label: "基础扫描",
          tips: "baseScan",
          fn: ({ row }) => {
            openPluginInfo.value.pluginName = "goby";

            openPluginInfo.value.assetName = row.asset_name;
            openPluginInfo.value.assetId = row.id;
            console.log(openPluginInfo.value);
            nextTick(() => {
              openPluginInfo.value.pluginName = "";
            });
          }
        },
        {
          label: "截图",
          tips: "screenShot",
          fn: row =>
            message(`您插件了第${row.rowIndex}行，数据为`, {
              type: "success"
            })
        },
        {
          label: "nucile",
          tips: "nucile",
          fn: row => console.log(row)
          // message(`您插件了第${row.rowIndex}行，数据为`, {
          //   type: "success"
          // })
        },
        {
          label: "yakit插件组",
          tips: "yakit",
          fn: row =>
            message(`您插件了第${row.rowIndex}行，数据为`, {
              type: "success"
            })
        }
      ]
    },
    {
      label: "发送到tag",
      tips: "Import",
      children: [
        {
          label: "A任务",
          tips: "tag1",
          fn: row =>
            message(`您发送了第${row.rowIndex}行，数据为`, {
              type: "success"
            })
        },
        {
          label: "重要处理",
          tips: "tag2",
          fn: row =>
            message(`您发送了第${row.rowIndex}行，数据为`, {
              type: "success"
            })
        }
      ]
    },
    {
      label: "导出笔记",
      tips: "Export",
      fn: row =>
        message(`您导出了第${row.rowIndex}行，数据为`, {
          type: "success"
        })
    },
    {
      label: "通知他人",
      tips: "broadcast",
      fn: row =>
        message(`您导出了第${row.rowIndex}行，数据为`, {
          type: "success"
        })
    }
  ]
};

function showMouseMenu(row, column, event) {
  event.preventDefault();
  const { x, y } = event;
  const ctx = CustomMouseMenu({
    el: event.currentTarget,
    params: { row: row, column: column },
    menuWidth: 150,
    // 菜单容器的CSS设置
    menuWrapperCss: {
      background: "var(--el-bg-color)",
      borderRadius: "10px"
    },
    menuItemCss: {
      labelColor: "var(--el-text-color)",
      hoverLabelColor: "var(--el-color-primary)",
      hoverTipsColor: "var(--el-color-primary)"
    },
    ...menuOptions
  });
  ctx.show(x, y);
}
// 菜单代码结束
</script>
<template>
  <div class="tablediv">
    <dialogCenter :openInfo="openPluginInfo" />
    <el-table
      v-if="ready"
      height="750px"
      style="border-radius: 12px"
      :data="rows"
      @row-contextmenu="showMouseMenu"
    >
      <!-- <el-table-column fixed type="expand" /> -->
      <el-table-column type="index" label="id" v-if="false" />
      <el-table-column
        fixed="left"
        property="asset_name"
        label="资产"
        width="200px"
        :loading="tableLoadingStatus"
      >
        <template #default="scope">
          <div>
            {{ scope.row.asset_name }}
            <el-icon style="margin-left: 5px"><ChatDotSquare /></el-icon>
          </div>
        </template>
      </el-table-column>
      <el-table-column
        fixed="left"
        label="关联资产"
        width="200px"
        :loading="tableLoadingStatus"
      >
        <template #default="scope">
          <div
            v-bind:key="textindex"
            v-for="(text, textindex) in scope.row.original_asset"
          >
            <el-text style="margin-right: 6px">{{ text }}</el-text>
            <el-icon style="top: 1px; cursor: pointer"
              ><Link style="margin-bottom: 3px" @click="openNewWindow(text)"
            /></el-icon>
          </div>
        </template>
      </el-table-column>
      <el-table-column
        v-for="(column, index) in columnInfo"
        :key="index"
        :label="column.label"
        :sortable="column.sort ? true : false"
      >
        <template #default="scope" v-if="column.type == 'Tag'">
          <el-scrollbar :height="maxCellHeight">
            <el-tag
              v-for="(tag, tagIndex) in scope.row.value[column.name].values"
              :key="tagIndex"
              :size="tag.attribute.size"
              :round="tag.attribute.round"
              :theme="tag.attribute.theme"
            >
              {{ tag.content }}
            </el-tag>
          </el-scrollbar>
        </template>
        <template #default="scope" v-else-if="column.type == 'Text'">
          <el-scrollbar :height="maxCellHeight">
            <el-text
              v-for="(text, textIndex) in scope.row.value[column.name].values"
              :key="textIndex"
              :size="text.attribute.size"
              :tag="text.attribute.tag"
              :type="text.attribute.type"
            >
              {{ text.content }}
              <br />
              ></el-text
            ></el-scrollbar
          >
        </template>
        <template #default="scope" v-else-if="column.type == 'Image'">
          <el-scrollbar :height="maxCellHeight">
            <el-image
              v-for="(image, imageIndex) in scope.row.value[column.name].values"
              :key="imageIndex"
              :src="image.content"
            />
          </el-scrollbar>
        </template>
      </el-table-column>
    </el-table>
    <div class="flexcontain">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next"
        :total="total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        style="margin-top: 1%"
      />
      <tableToolBar />
    </div>
  </div>
</template>
<style scoped>
.flexcontain {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1%;
}
.tablediv {
  border-radius: 12px;
}
</style>

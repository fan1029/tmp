<script setup lang="ts">
import { ref, nextTick, watch, onMounted, onUnmounted } from "vue";
import { useTagStoreHook } from "@/store/modules/tag";
import { CustomMouseMenu } from "@howdyjs/mouse-menu";
import { message } from "@/utils/message";
import { Link } from "@element-plus/icons-vue";
import dialogCenter from "@/views/console/components/pluginDialog/index.vue";
import tableToolBar from "@/views/console/components/tableToolBar/index.vue";
import { deleteTagApi } from "@/api/tag";
import { getConfig } from "@/config";
import NoteSmall from "@/views/console/components/note/note_small.vue";
// ###COL组件
import asset_name_Col from "./tableComponents/asset_name_Col.vue";

//接受父组件传来的tag_id参数
// 表格数据代码
const maxCellHeight = "150px"; //单元格最大高度
const props = defineProps(["tag_id"]); //tag_id
const tagStore = useTagStoreHook(); //pinia
const openPluginInfo = ref({
  pluginName: "",
  assetName: "",
  assetId: -1,
  tag_id: props.tag_id
}); //插件弹窗信息
const columnInfo = ref([]);
const rows = ref([]);
const total = ref(0);
const pageSize = ref(10); //每页显示多少条
const currentPage = ref(1); //当前页
const sort = ref("asc"); //排序方式
const sortColumn = ref("asset_original"); //排序字段
const tableLoadingStatus = ref(true); //表格加载状态
const wsServerHost = "ws://" + getConfig().serverHost + "/tag/syncTable"; //服务器地址
// #####################################   websocket重写 ##########################

function syncTable(socket) {
  const sendData = {
    project_id: tagStore.project_id,
    tag_id: props.tag_id,
    tag_name: "",
    size: pageSize.value,
    page: currentPage.value,
    sort: sort.value,
    sortColumn: sortColumn.value,
    current_table: []
  };
  const myJSON = JSON.stringify(sendData);
  try {
    socket.send(myJSON);
  } catch (error) {
    console.log("websocket连接发生错误");
    socket = new WebSocket(wsServerHost);
  }
}

let socket = new WebSocket(wsServerHost);
socket.onopen = function () {
  console.log("websocket已连接");
  syncTable(socket);
};

socket.onclose = function () {
  // 重连
  setTimeout(() => {
    console.log("websocket已关闭");
    socket = new WebSocket(wsServerHost);
  }, 300);
};

socket.onmessage = function (event) {
  try {
    const data = JSON.parse(event.data);
    if (data.msg == "hello") {
      message("同步服务已连接", {
        type: "success"
      });
    } else {
      columnInfo.value = data.data.column;
      rows.value = data.data.rows;
      total.value = data.total;
      tableLoadingStatus.value = false;
      console.log(columnInfo.value);
    }
  } catch (error) {
    console.log(error);
  }
};

onMounted(() => {
  setInterval(() => {
    syncTable(socket);
  }, 10000);
});

onUnmounted(() => {
  socket.close();
});

function delAssetFromTag(asset_id: number) {
  deleteTagApi({
    project_id: Number(tagStore.project_id),
    tag_id: Number(props.tag_id),
    asset_id: Number(asset_id)
  })
    .then(() => {
      message("删除成功", {
        type: "success"
      });
      syncTable(socket);
    })
    .catch(() => {
      message("删除失败", {
        type: "error"
      });
    });
}

function handleSizeChange(val: number) {
  pageSize.value = val;
  tableLoadingStatus.value = true;
  syncTable(socket);
}
function handleCurrentChange(val: number) {
  currentPage.value = val;
  syncTable(socket);
}

function openNewWindow(url: string) {
  // 新建窗口打开该连接，不是拼接在现有Url后面，没有http://则添加访问
  if (!url.startsWith("http")) {
    url = "http://" + url;
  }
  window.open(url);
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
      fn: ({ row }) => {
        delAssetFromTag(row.id);
      }
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
          fn: ({ row }) => {
            openPluginInfo.value.pluginName = "Plugin_screenShot";

            openPluginInfo.value.assetName = row.asset_name;
            openPluginInfo.value.assetId = row.id;
            console.log(openPluginInfo.value);
            nextTick(() => {
              openPluginInfo.value.pluginName = "";
            });
          }
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

const rowColorStyle = ({ row, rowIndex }) => {
  console.log(row);
  switch (row.row_color) {
    case "red":
      return "background-color: #ffcccc";
    case "yellow":
      return "background-color: #ffffcc";
    case "green":
      return "background-color: #ccffcc";
    default:
      return "";
  }
};
</script>
<template>
  <div class="tablediv">
    <NoteSmall />
    <dialogCenter :openInfo="openPluginInfo" />
    <el-table
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
        <template #default="scope"><asset_name_Col :scope="scope" /></template>
      </el-table-column>
      <el-table-column
        label="web资产"
        width="200px"
        :loading="tableLoadingStatus"
      >
        <template #default="scope">
          <div
            v-bind:key="textindex"
            v-for="(text, textindex) in scope.row.original_assets"
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
              v-for="(tag, tagIndex) in scope.row[column.name].values"
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
              v-for="(text, textIndex) in scope.row[column.name].values"
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
          <div>
            <el-carousel :interval="5000" :height="maxCellHeight">
              <el-carousel-item
                v-for="(image, imageIndex) in scope.row[column.name].values"
                :key="imageIndex"
              >
                <img
                  id="images"
                  :src="image.content"
                  @click="handlePictureCardPreview(image.content)"
                />
              </el-carousel-item>
            </el-carousel>
          </div>
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
      <tableToolBar :tag_id="props.tag_id" :project_id="tagStore.project_id" />
    </div>
  </div>
</template>
<style scoped>
.el-tooltip__trigger {
  display: inline-block;
}
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

// import { ref } from "vue";
import { message } from "@/utils/message";
import { CustomMouseMenu } from "@howdyjs/mouse-menu";
import { fetchData } from "@/api/tableData";
import { useTableDataStore } from "@/store/modules/tableData";

export function useColumns() {
  const tableDataList = useTableDataStore();
  // const tableDataList = tableDataList2.tableData;
  // console.log(tableDataList);
  // const tableDataList = ref([]);
  // const columns2 = ref([
  //   { prop: "url", label: "Url", sort: "true" },
  //   { prop: "ip", label: "Ip" },
  //   { prop: "tag", label: "Tag", template: "tag" },
  //   { prop: "screenShoot", label: "ScreenShoot", template: "img" }
  // ]);

  // const tableDataList = ref([]);

  const menuOptions = {
    menuList: [
      {
        label: ({ row }) => `URL：${row.url}`,
        disabled: true
      },
      {
        label: "标记",
        children: [
          {
            label: "红",
            fn: ({ row, column1 }) =>
              message(`标记红色：${row.url} - ${column1}`)
          },
          {
            label: "绿",
            fn: ({ row, column1 }) =>
              message(`标记红色：${row.url} - ${column1}`)
          },
          {
            label: "蓝",
            fn: ({ row, column1 }) =>
              message(`标记红色：${row.url} - ${column1}`)
          },
          {
            label: "黄",
            fn: ({ row, column1 }) =>
              message(`标记红色：${row.url} - ${column1}`)
          },
          {
            label: "取消标记",
            fn: ({ row, column1 }) =>
              message(`标记红色：${row.url} - ${column1}`)
          }
        ]
      },
      {
        label: "删除",
        fn: ({ row, column1 }) => message(`删除：${row.url}`)
      },
      {
        label: "插件",
        tip: "结果不上表",
        children: [
          {
            label: "子域名收集",
            fn: ({ row, column1 }) => message(`子域名收集：${row.url}`)
          },
          {
            label: "目录扫描",
            fn: ({ row, column1 }) => message(`目录扫描：${row.url}`)
          }
        ]
      },
      {
        label: "扫描",
        tip: "scan",
        children: [
          {
            label: "nuclei",
            fn: ({ row, column1 }) => message(`nuclei：${row.url}`)
          },
          {
            label: "xray",
            fn: ({ row, column1 }) => message(`xray：${row.url}`)
          }
        ]
      }
    ]
  };

  function showMouseMenu(row, column, event) {
    event.preventDefault();
    const { x, y } = event;
    const ctx = CustomMouseMenu({
      el: event.currentTarget,
      params: { row: row, column1: column },
      // 菜单容器的CSS设置
      menuWrapperCss: {
        background: "#ffffff",
        borderRadius: "8px",
        padding: "8px 6px",
        boxShadow: "0 2px 12px 0 rgba(0,0,0,.1)",
        lineColor: "#eee",
        lineMargin: "5px 10px"
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

  async function getTableData(currentPage: number, pageSize: number) {
    return new Promise((resolve, reject) => {
      fetchData(currentPage, pageSize)
        .then(res => {
          tableDataList.tableData = res.data;
          // console.log(tableDataList);
          resolve(res);
        })
        .catch(err => {
          reject(err);
        });
    });
  }

  // async function getTableData(currentPage: number, pageSize: number) {
  //   return new Promise((resolve, reject) => {
  //     fetchData(currentPage, pageSize)
  //       .then(res => {
  //         tableDataList.value = res.data;
  //         resolve(res);
  //       })
  //       .catch(err => {
  //         reject(err);
  //       });
  //   });
  // }

  return {
    tableDataList,
    getTableData,
    showMouseMenu
  };
}

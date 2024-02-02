import { store } from "@/store";
import { defineStore } from "pinia";

export const useTableDataStore = defineStore("tableData", {
  state: () => ({
    tableData: [],
    columns: [
      { prop: "url", label: "Url", sort: "true" },
      { prop: "ip", label: "Ip" },
      { prop: "tag", label: "Tag", template: "tag" },
      { prop: "screenShoot", label: "ScreenShoot", template: "img" }
    ]
  }),
  getters: {
    getTableData: state => state.tableData
  },
  actions: {
    setTableData(data) {
      this.tableData = data;
    }
  }
});

export function useTableDataStoreHook() {
  return useTableDataStore(store);
}

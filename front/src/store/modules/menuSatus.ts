import { store } from "@/store";
import { defineStore } from "pinia";

export const useMenuStatusStore = defineStore("menuStatus", {
  state: () => ({
    tmp: 0,
    currentUsers: [],
    taskInfo: {},
    serviceStatus: [],
    systemInfo: {},
    TaskCount: {}
  }),
  getters: {},
  actions: {
    setInfoData(websocketData: any) {
      switch (websocketData.from) {
        case "getSystemInfo":
          this.systemInfo = websocketData.data;
          break;
        case "getTaskCount":
          this.taskInfo = websocketData.data;
          break;
        case "getServiceStatus":
          this.serviceStatus = websocketData.data;
          break;
        case "system":
          this.systemInfo = websocketData.data;
          break;
      }
    }
  }
});

export function useMenuStatusStoreHook() {
  return useMenuStatusStore(store);
}

import { ElMessage, ElNotification } from "element-plus";
import { getConfig } from "@/config";

const wsServer = "ws://" + getConfig().serverHost + "/notify";
export function startNotifyService() {
  const notifySocket = new WebSocket(wsServer);
  notifySocket.onopen = () => {
    ElMessage.success("通知服务连接成功");
  };
  notifySocket.onerror = () => {
    ElMessage.error("通知服务连接失败");
    // 重连
    setTimeout(() => {
      startNotifyService();
    }, 5000);
  };
  notifySocket.onmessage = e => {
    const data = JSON.parse(e.data);
    console.log(data);
    // if (data.msg) {
    //   console.log(data.msg);
    // }
    if (data.time) {
      console.log(data);
      if (data.displayType == "ElMessage") {
        if (data.type == "success") {
          ElMessage.success(data.content);
        } else if (data.type == "warning") {
          ElMessage.warning(data.content);
        } else if (data.type == "error") {
          ElMessage.error(data.content);
        } else if (data.type == "info") {
          ElMessage.info(data.content);
        }
      } else if (data.displayType == "ElNotification") {
        if (data.type == "success") {
          ElNotification.success({
            title: data.title,
            message: data.content
          });
        } else if (data.type == "warning") {
          ElNotification.warning({
            title: data.title,
            message: data.content
          });
        } else if (data.type == "error") {
          ElNotification.error({
            title: data.title,
            message: data.content
          });
        } else if (data.type == "info") {
          ElNotification.info({
            title: data.title,
            message: data.content
          });
        }
      }
    }
  };
  return notifySocket;
}

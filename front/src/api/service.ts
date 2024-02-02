import { http } from "@/utils/http";

export const getServiceSatatusApi = () => {
  return http.request("get", "/service/getServiceSatatus");
};

export const changeServiceStatusApi = (data: any) => {
  return http.request("post", "/service/changeServiceStatus", { data });
};

export const runPluginApi = (data: any) => {
  return http.request("post", "/service/runPlugin", { data });
};

export const getPluginInfoApi = (data: any) => {
  return http.request("post", "/service/getPluginInfo", { data });
};

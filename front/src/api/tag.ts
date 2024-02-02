import { http } from "@/utils/http";
// import { info } from "console";

export type GetAssetDataRequest = {
  /** 项目id */
  project_id: number;
  /** 标签名 */
  tag_id: number;
  size: number;
  page: number;
  sort: string;
  tag_name: string;
  sortColumn: string;
  current_table: string[];
};

export interface Data {
  asset_original: string[];
  column: Column[];
  rows: Row[];
}

export interface Column {
  edit: boolean;
  hide: boolean;
  label: string;
  max_width: null;
  name: string;
  pluginName: string;
  sort: boolean;
  type: string;
}

export interface Row {
  id: number;
  asset_original: string;
  color: string;
  value: RowValue;
}

export interface RowValue {
  port: Port;
  tag: Tag;
  vul: Vul;
}

export interface Port {
  elementType: string;
  style: AttributeClass;
  values: PortValue[];
}

export interface AttributeClass {
  round: boolean;
  size: string;
  theme: string;
}

export interface PortValue {
  action: PurpleAction;
  attribute: AttributeClass;
  content: string;
  elementType: string;
}

export interface PurpleAction {
  click: null;
  hover: null;
}

export interface Tag {
  elementType: string;
  style: AttributeClass;
  values: TagValue[];
}

export interface TagValue {
  action: FluffyAction;
  attribute: AttributeClass;
  content: string;
  elementType: string;
}

export interface FluffyAction {
  click: Click;
  hover: null;
}

export interface Click {
  attribute: Attribute;
  content: string;
  elementType: string;
  title: string;
}

export interface Attribute {
  placement: string;
  theme: string;
}

export interface Vul {
  elementType: string;
  style: VulStyle;
  values: any[];
}

export interface VulStyle {
  size: string;
  tag: string;
  type: string;
}

export interface Info {
  current_table: string[];
  page: number;
  project_id: number;
  size: number;
  sort: string;
  sortColumn: string;
  tag_id: number;
  tag_name: string;
  total: number;
}

export interface GetAssetDataResult {
  data: Data;
  info: Info;
  msg: string;
  status: boolean;
}
export const getAssetData = (data: GetAssetDataRequest) => {
  return http.request<GetAssetDataResult>("post", "tag/getAssetData2", {
    data
  });
};

export interface GetTagListResult {
  data: Datum[];
  msg: string;
  status: boolean;
}

export interface Datum {
  create_time: string;
  create_user: string;
  description: string;
  id: number;
  project_id: number;
  tag_name: string;
}

export const getTagList = (data: { projectId: number }) => {
  return http.request<GetTagListResult>("post", "project/getProjectTag", {
    data
  });
};

export const addAssetToTagApi = (data: any) => {
  return http.request("post", "tag/addAssetToTag", { data });
};

export const deleteAssetFromTagApi = (data: any) => {
  return http.request("post", "tag/deleteAssetFromTag", { data });
};

export const deleteTagApi = (data: any) => {
  return http.request("post", "tag/deleteAssetFromTag", { data });
};

import { store } from "@/store";
import { defineStore } from "pinia";
import { getAssetData, Data, Row, getTagList } from "@/api/tag";

export type Tag = {
  id: number;
  name: string;
  create_user?: string;
  create_time?: string;
  description?: string;
  data?: Data;
  total?: number;
};

export const useTagStore = defineStore("tag", {
  state: () => ({
    project_id: -1,
    //新建一个sring,Tag类型的Map
    tagMap: new Map<string, Tag>()
  }),
  getters: {},
  actions: {
    setProjectId(project_id: number) {
      this.project_id = project_id;
    },
    // 添加标签
    addTag(tag_id: string) {
      this.tagMap.set(tag_id, {
        id: 0,
        name: "",
        data: Date()
      });
    },
    //获取标签对象
    getTagByName(name: string) {
      return this.tagMap.get(name);
    },
    getTagById(id: number) {
      return this.tagMap.get(id.toString());
    },
    //获取所有标签名
    getTagNameList() {
      return Array.from(this.tagMap.keys());
    },
    getTagInfoList() {
      //遍历map获取所有id 以name组成数组
      const tagInfoList = [];
      for (const [key, value] of this.tagMap) {
        tagInfoList.push({
          id: value.id,
          name: value.name
        });
      }
      return tagInfoList;
    },
    //设置标签MAP
    setTagMap(tagMap: Map<string, Tag>) {
      this.tagMap = tagMap;
    },
    //清除标签页
    clearTagMap() {
      this.tagMap.clear();
    },
    //删除标签
    deleteTag(name: string) {
      this.tagMap.delete(name);
    },
    //清除标签内的资产内容
    clearAssetMap(tagName: string) {
      const tag = this.getTag(tagName);
      tag.data.clear();
    },
    //标签内添加资产
    addAsset(tagName: string, row: Row) {
      const tag = this.getTag(tagName);
      tag.data.rows.push(row);
    },
    setAssetMap(tagName: string, data: Data) {
      const tag = this.getTag(tagName);
      tag.data = data;
    },
    //删除资产row
    deleteAsset(tagName: string, asset_original: string) {
      const tag = this.getTag(tagName);
      //遍历tag.data.rows,asset_original,并删除
      tag.data.rows.forEach((row, index) => {
        if (row.asset_original == asset_original) {
          tag.data.rows.splice(index, 1);
        }
      });
    },
    //获取列数据
    getColumn(tag_id: string) {
      const tag = this.getTagById(tag_id);
      return tag.data.column;
    },
    //获取行数据
    getRows(tag_id: string) {
      const tag = this.getTagById(tag_id);
      return tag.data.rows;
    },
    async getTagInfoQuery() {
      const tagInfoList = await getTagList({ projectId: this.project_id });
      const data = tagInfoList.data;
      // const tagMap = new Map<string, Tag>();
      data.forEach(tagInfo => {
        this.tagMap.set(tagInfo.id.toString(), {
          id: tagInfo.id,
          name: tagInfo.tag_name,
          create_user: tagInfo.create_user,
          create_time: tagInfo.create_time,
          description: tagInfo.description
        });
      });
      //遍历tagInfoList,并创建tag
    },

    //请求api获取该项目所有的tagName,并创建tag
    async getAssetDataQuery(
      tag_id: number,
      size = 10,
      page = 1,
      sort = "asc",
      sortColumn = "asset_original",
      tag_name = "",
      current_table = []
    ) {
      const assetData = await getAssetData({
        project_id: this.project_id,
        tag_id: tag_id,
        size: size,
        page: page,
        sort: sort,
        tag_name: tag_name,
        sortColumn: sortColumn,
        current_table: current_table
      });
      //获取id为tag_id的tag
      // this.addTag(assetData.info.tag_id.toString());
      const tag = this.getTagById(tag_id.toString());
      //设置tag的data

      tag.data = assetData.data;
      tag.name = assetData.info.tag_name;
      tag.id = assetData.info.tag_id;
      tag.total = assetData.info.total;
    }
  }
});

export function useTagStoreHook() {
  return useTagStore(store);
}

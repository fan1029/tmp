import { defineStore } from "pinia";

export const useProjectEnvStore = defineStore("projectEnv", () => ({
  state: () => ({
    project_id: 0
  }),
  getters: {
    getProjectId(state) {
      return state.project_id;
    },
    getTagId(state) {
      return state.tag_id;
    },
    getSize(state) {
      return state.size;
    },
    getPage(state) {
      return state.page;
    },
    getSort(state) {
      return state.sort;
    },
    getTagName(state) {
      return state.tag_name;
    },
    getSortColumn(state) {
      return state.sortColumn;
    }
  },
  actions: {
    setProjectId(project_id) {
      this.project_id = project_id;
    },
    setTagId(tag_id) {
      this.tag_id = tag_id;
    },
    setSize(size) {
      this.size = size;
    },
    setPage(page) {
      this.page = page;
    },
    setSort(sort) {
      this.sort = sort;
    },
    setTagName(tag_name) {
      this.tag_name = tag_name;
    },
    setSortColumn(sortColumn) {
      this.sortColumn = sortColumn;
    }
  }
}));

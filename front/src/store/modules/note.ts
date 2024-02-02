import { defineStore } from "pinia";

export const useNoteStore = defineStore("note", {
  state: () => ({
    currentAssetIDForNote: -1,
    currentAssetNameForNote: ""
  }),
  getters: {},
  actions: {
    setCurrentNoteId(assetId: number) {
      this.currentAssetIDForNote = assetId;
    },
    setCurrentNoteName(assetName: string) {
      this.currentAssetNameForNote = assetName;
    }
  }
});

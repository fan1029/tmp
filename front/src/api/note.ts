import { http } from "@/utils/http";

export const getNoteListApi = () => {
  return http.request("get", "note/getNoteList");
};

export const openNoteApi = (data: any) => {
  return http.request("post", "note/openNote", { data });
};

export const saveNoteApi = (data: any) => {
  return http.request("post", "note/saveNote", { data });
};

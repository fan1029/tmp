import { http } from "@/utils/http";

type Project = {
  /** 项目id */
  id: number;
  /** 项目名称 */
  name: string;
  /** 项目描述 */
  description: string;
  /** 项目创建时间 */
  create_time: Date;
  /** 项目创建人 */
};

export type ProjectListResult = {
  status: number;
  data: Project[];
};

export const getProjectList = () => {
  return http.request<ProjectListResult>("get", "project/getProjectList");
};

export type ProjectCreateRequest = {
  /** 项目名称 */
  name: string;
  /** 项目描述 */
  description: string;
  assets: string[];
  /** 项目创建人 */
  createUser: string;
};

type ProjectCreateResult = {
  status: boolean;
  msg: string;
  create_time: string;
  project_id: number;
};
export const createProject = (data: ProjectCreateRequest) => {
  return http.request<ProjectCreateResult>("post", "project/createProject", {
    data
  });
};

export type getProjectTagRequest = {
  projectId: number;
};
type TagInfo = {
  id: number;
  project_id: number;
  tag_name: string;
  description: string;
  create_time: string;
  create_user: string;
  used_plugin: string[];
};

export type getProjectTagResult = {
  status: boolean;
  msg: string;
  data: TagInfo[];
};

export const getProjectTag = (data: getProjectTagRequest) => {
  return http.request<getProjectTagResult>("post", "project/getProjectTag", {
    data
  });
};

export type createTagRequest = {
  project_id: number;
  tag_name: string;
  create_user: string;
  description: string;
  asset: string[];
};
export type createTagResult = {
  status: boolean;
  msg: string;
  data: createTagRequest & object;
};
export const createProjectTag = (data: createTagRequest) => {
  return http.request<createTagResult>("post", "tag/createTag", {
    data
  });
};

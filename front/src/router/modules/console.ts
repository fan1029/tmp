// const { VITE_HIDE_HOME } = import.meta.env;

export default {
  path: "/console",
  name: "工作台",
  // redirect: "/console",
  component: () => import("@/views/console/console.vue"),
  meta: {
    icon: "homeFilled",
    title: "工作台",
    rank: 0
  },
  children: [
    {
      path: "/console",
      name: "console",
      component: () => import("@/views/console/console.vue"),
      meta: {
        title: "工作台"
        // showLink: VITE_HIDE_HOME === "true" ? false : true
      }
    }
  ]
} as RouteConfigsTable;

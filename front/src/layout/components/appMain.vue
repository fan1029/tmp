<script setup lang="ts">
import { useGlobal } from "@pureadmin/utils";
import backTop from "@/assets/svg/back_top.svg?component";
import { h, computed, Transition, defineComponent } from "vue";
import { onMounted } from "vue";
import { emitter } from "@/utils/mitt";

// import { Console } from "console";
import { usePermissionStoreHook } from "@/store/modules/permission";

const props = defineProps({
  fixedHeader: Boolean
});

const { $storage, $config } = useGlobal<GlobalPropertiesApi>();

const isKeepAlive = computed(() => {
  return $config?.KeepAlive;
});
const transitions = computed(() => {
  return route => {
    return route.meta.transition;
  };
});

onMounted(() => {
  const storageConfigure = $storage.configure;
  storageConfigure["hideTabs"] = true;
  $storage.configure = storageConfigure;
  console.log($storage.configure);
  emitter.emit("tagViewsChange", true as unknown as string);
});

const hideTabs = computed(() => {
  // $storage.configure.hideTabs = true;
  return $storage?.configure.hideTabs;
});

const layout = computed(() => {
  return $storage?.layout.layout === "vertical";
});

const getSectionStyle = computed(() => {
  return [
    hideTabs.value && layout ? "padding-top: 0px;" : "",
    !hideTabs.value && layout ? "padding-top: 85px;" : "",
    hideTabs.value && !layout.value ? "padding-top: 0px" : "",
    !hideTabs.value && !layout.value ? "padding-top: 85px;" : "",
    props.fixedHeader ? "" : "padding-top: 0;"
  ];
});

const transitionMain = defineComponent({
  render() {
    return h(
      Transition,
      {
        name:
          transitions.value(this.route) &&
          this.route.meta.transition.enterTransition
            ? "pure-classes-transition"
            : (transitions.value(this.route) &&
                this.route.meta.transition.name) ||
              "fade-transform",
        enterActiveClass:
          transitions.value(this.route) &&
          `animate__animated ${this.route.meta.transition.enterTransition}`,
        leaveActiveClass:
          transitions.value(this.route) &&
          `animate__animated ${this.route.meta.transition.leaveTransition}`,
        mode: "out-in",
        appear: true
      },
      {
        default: () => [this.$slots.default()]
      }
    );
  },
  props: {
    route: {
      type: undefined,
      required: true
    }
  }
});
</script>

<template>
  <section
    :class="[props.fixedHeader ? 'app-main' : 'app-main-nofixed-header']"
    :style="getSectionStyle"
  >
    <router-view>
      <template #default="{ Component, route }">
        <el-scrollbar v-if="props.fixedHeader">
          <el-backtop title="回到顶部" target=".app-main .el-scrollbar__wrap">
            <backTop />
          </el-backtop>
          <transitionMain :route="route">
            <keep-alive
              v-if="isKeepAlive"
              :include="usePermissionStoreHook().cachePageList"
            >
              <component
                :is="Component"
                :key="route.fullPath"
                class="main-content"
              />
            </keep-alive>
            <component
              v-else
              :is="Component"
              :key="route.fullPath"
              class="main-content"
            />
          </transitionMain>
        </el-scrollbar>
        <div v-else>
          <transitionMain :route="route">
            <!-- **修改：全部可缓存 -->
            <!-- <keep-alive
              v-if="isKeepAlive"
              :include="usePermissionStoreHook().cachePageList"
            > -->
            <keep-alive>
              <component
                :is="Component"
                :key="route.fullPath"
                class="main-content"
              />
            </keep-alive>
            <!-- <component
              v-else
              :is="Component"
              :key="route.fullPath"
              class="main-content"
            /> -->
          </transitionMain>
        </div>
      </template>
    </router-view>
  </section>
</template>

<style scoped>
/* 修改 */
.app-main {
  position: relative;
  width: 100%;
  height: 90vh;
  overflow-x: hidden;
}

.app-main-nofixed-header {
  position: relative;
  width: 100%;
  min-height: 100vh;
}

.main-content {
  margin: 24px;
}
</style>

<script setup lang="ts">
import gobyScanDialog from "./goby.vue";
import screenShot from "./screenShot.vue";
import { defineProps } from "vue";
const prop = defineProps(["openInfo"]);
</script>

<template>
  <div>
    <gobyScanDialog :openInfo="prop.openInfo" />
    <screenShot :openInfo="prop.openInfo" />
  </div>
</template>

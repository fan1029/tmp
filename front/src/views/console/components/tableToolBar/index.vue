<script setup lang="ts">
import { DeleteFilled, Plus, Download } from "@element-plus/icons-vue";
import { addAssetToTagApi } from "@/api/tag";
import { ref, defineProps } from "vue";
import { ElMessage } from "element-plus";
const addAssetVisible = ref(false);
const asset_add = ref("");
const props = defineProps({
  tag_id: {
    type: Number,
    required: true
  },
  project_id: {
    type: Number,
    required: true
  }
});
function addNewAsset() {
  console.log(asset_add.value);
  addAssetToTagApi({
    tag_id: props.tag_id,
    project_id: props.project_id,
    asset: asset_add.value.split("\n")
  }).then(res => {
    ElMessage.info(res.msg);
    console.log(res);
  });
}
</script>
<template>
  <div>
    <el-dialog
      title="添加资产"
      v-model="addAssetVisible"
      width="30%"
      style="border-radius: 12px"
    >
      <el-form>
        <el-form-item label="资产">
          <el-input
            type="textarea"
            v-model="asset_add"
            :autosize="{ minRows: 10, maxRows: 20 }"
            placeholder="一行一个，记得最后一行不要换行~"
          />
        </el-form-item>
        <el-form-item>
          <div style="margin-left: auto; display: block">
            <el-button
              type="primary"
              @click="
                addAssetVisible = false;
                addNewAsset();
              "
            >
              确定
            </el-button>
            <el-button @click="addAssetVisible = false">取消</el-button>
          </div>
        </el-form-item>
      </el-form>
    </el-dialog>
    <el-tooltip content="添加资产" placement="top" effect="light">
      <el-button
        type="primary"
        circle
        :icon="Plus"
        size="large"
        @click="addAssetVisible = !addAssetVisible"
      />
    </el-tooltip>
    <el-tooltip content="导出数据" placement="top" effect="light">
      <el-button type="success" circle :icon="Download" size="large" />
    </el-tooltip>
    <el-tooltip content="删除本页" placement="top" effect="light">
      <el-button type="danger" circle :icon="DeleteFilled" size="large" />
    </el-tooltip>
  </div>
</template>

<template>
  <div class="tablediv">
    <el-table
      :data="tableDataList.tableData"
      @row-contextmenu="showMouseMenu"
      max-height="700px"
      style="border-radius: 20px"
    >
      <el-table-column fixed type="expand">
        <template #default="props">
          <div m="4">
            <h3>test1123</h3>
          </div>
        </template>
      </el-table-column>
      <el-table-column
        v-for="(column, index) in tableDataList.columns"
        :key="index"
        :property="column.prop"
        :label="column.label"
        :sortable="column.sort ? true : false"
        :fixed="column.label === 'Url' ? 'left' : false"
      >
        <template #default="scope" v-if="column.template == 'tag'">
          <el-tag
            v-for="(tag, tagIndex) in dynamicTags[scope.$index]"
            :key="tagIndex"
            class="mx-1"
            closable
            :disable-transitions="false"
            @close="handleClose(scope.$index, tagIndex)"
          >
            {{ tag }}
          </el-tag>
          <el-input
            v-if="inputVisible[scope.$index]"
            :ref="'InputRef' + scope.$index"
            v-model="inputValue[scope.$index]"
            class="ml-1 w-20"
            size="small"
            @keyup.enter="handleInputConfirm(scope.$index)"
            @blur="handleInputConfirm(scope.$index)"
            width="30px"
          />
          <el-button
            v-else
            class="button-new-tag ml-1"
            size="small"
            @click="showInput(scope.$index)"
          >
            + New Tag
          </el-button>
        </template>
        <template #default="scope" v-else-if="column.template == 'button'"
          ><h1>{{ scope.row.id }}</h1></template
        >
        <template #default="scope" v-else-if="column.template == 'img'">
          <div class="block">
            <el-table
              :data="tableData2"
              max-height="150px"
              :show-header="false"
              style="border-radius: 20px"
            >
              <el-table-column prop="date" label="Date" />
              <el-table-column prop="name" label="Name" />
              <el-table-column prop="address" label="Address" />
            </el-table>

            <!-- <el-image
              style="width: 120px; height: 100px"
              :src="'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg'"
            /> -->
          </div>
        </template>
      </el-table-column>
      <el-table-column
        width="200px"
        fixed="right"
        property="buttonOpitions"
        label="操作"
      >
        <template #default="scope">
          <el-button size="small">预留</el-button>
          <el-button size="small">预留</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
  <div class="page_div">
    <el-pagination
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      :page-sizes="[10, 20, 50, 100]"
      :small="small"
      :disabled="disabled"
      :background="background"
      layout="total, sizes, prev, pager, next"
      :total="total"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      style="margin-top: 1%; margin-left: 60%"
    />
  </div>
</template>

<script setup lang="ts">
import { useColumns } from "../columns";
const { tableDataList, getTableData, showMouseMenu } = useColumns();
// const props = defineProps(["tableData", "columns"]);
import { nextTick, ref } from "vue";
import { ElInput } from "element-plus";
import { onMounted } from "vue";
const inputValue = ref([]);
const dynamicTags = ref([]);
const inputVisible = ref([]);
const InputRef = ref([]);
//分页
// const tableData = ref([]);
const currentPage = ref(1);
const pageSize = ref(10);
const total = ref(100);
const small = ref(false);
const background = ref(false);
const disabled = ref(false);
const tableData2 = [
  {
    date: "2016-05-03",
    name: "Tom",
    address: "No. 189, "
  },
  {
    date: "2016-05-02",
    name: "Tom",
    address: "No. 189,"
  },
  {
    date: "2016-05-04",
    name: "Tom",
    address: "No. 189, G Angeles"
  },
  {
    date: "2016-05-01",
    name: "Tom",
    address: "No. 18es"
  }
];
const handleSizeChange = (val: number) => {
  pageSize.value = val;
  getTableData(currentPage.value, pageSize.value);
};
const handleCurrentChange = (val: number) => {
  currentPage.value = val;
  getTableData(currentPage.value, pageSize.value);
  console.log(tableDataList);
};
//1
// console.log(tableDataList.value.length);
for (let i = 0; i < tableDataList.tableData.length; i++) {
  console.log(tableDataList.length);
  inputValue.value.push("");
  dynamicTags.value.push(["Tag 1"]);
  inputVisible.value.push(false);
  InputRef.value.push(ref<InstanceType<typeof ElInput>>());
}

onMounted(() => {
  getTableData(currentPage.value, pageSize.value);
  // console.log(tableDataList);
});

const handleClose = (rowIndex: number, tagIndex: number) => {
  dynamicTags.value[rowIndex].splice(tagIndex, 1);
};

const showInput = (rowIndex: number) => {
  inputVisible.value[rowIndex] = true;
  nextTick(() => {
    InputRef.value[rowIndex].value!.input!.focus();
  });
};

const handleInputConfirm = (rowIndex: number) => {
  if (inputValue.value[rowIndex]) {
    dynamicTags.value[rowIndex].push(inputValue.value[rowIndex]);
  }
  inputVisible.value[rowIndex] = false;
  inputValue.value[rowIndex] = "";
};
</script>
<style scoped>
.demo-pagination-block + .demo-pagination-block {
  margin-top: 10px;
}
.demo-pagination-block .demonstration {
  margin-bottom: 16px;
}
.tablediv {
  margin-left: 8%;
  margin-right: 1%;
  border-radius: 20px;
}
</style>

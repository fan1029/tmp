<script setup lang="ts">
import { ref, watch, defineProps } from "vue";
import { runPluginApi, getPluginInfoApi } from "@/api/service";
import { ElMessage } from "element-plus";
const pluginName = "plugin_goby";
const p = defineProps(["openInfo"]);
const gobyopenStatus = ref(false);
const currentTarget = ref({ id: -1, asset_name: "" });
watch(
  () => {
    try {
      return p.openInfo.pluginName;
    } catch (error) {
      return "";
    }
  },
  val => {
    if (val == "goby") {
      gobyopenStatus.value = true;
      currentTarget.value.id = p.openInfo.assetId;
      currentTarget.value.asset_name = p.openInfo.assetName;
      getPluginInfoApi({ pluginName: pluginName }).then(res => {
        pluginInfo.value = res.data;
      });
    }
  }
);
const pluginInfo = ref({});

const scanRate = ref(500);
const region = ref("asset_selected");
const portType = ref("portType1");
const portType1Conent =
  "21,22,23,25,53,U:53,U:69,80,81,U:88,110,111,U:111,123,U:123,135,U:137,139,U:161,U:177,389,U:427,443,445,465,500,515,U:520,U:523,548,623,U:626,636,873,902,1080,1099,1433,U:1434,1521,U:1604,U:1645,U:1701,1883,U:1900,2049,2181,2375,2379,U:2425,3128,3306,3389,4730,U:5060,5222,U:5351,U:5353,5432,5555,5601,5672,U:5683,5900,5938,5984,6000,6379,7001,7077,8080,8081,8443,8545,8686,9000,9001,9042,9092,9100,9200,9418,9999,11211,U:11211,27017,U:33848,37777,50000,50070,61616";
const portType2Content =
  "21,22,80,U:137,U:161,443,445,U:1900,3306,3389,U:5353,8080";
const portType3Content =
  "U:523,1433,U:1434,1521,1583,2100,2049,U:2638,3050,3306,3351,5000,5432,5433,5601,5984,6082,6379,7474,8080,8088,8089,8098,8471,9000,9160,9200,9300,9471,11211,U:11211,15672,19888,27017,27019,27080,28017,50000,50070,50090";
const portType4Content =
  "1,7,9,13,19,21-23,25,37,42,49,53,69,79-81,85,105,109-111,113,123,135,137-139,143,161,179,222,264,384,389,402,407,443-446,465,500,502,512-515,523-524,540,548,554,587,617,623,689,705,771,783,873,888,902,910,912,921,993,995,998,1000,1024,1030,1035,1090,1098-1103,1128-1129,1158,1199,1211,1220,1234,1241,1300,1311,1352,1433-1435,1440,1494,1521,1530,1533,1581-1582,1604,1720,1723,1755,1811,1900,2000-2001,2049,2082,2083,2100,2103,2121,2199,2207,2222,2323,2362,2375,2380-2381,2525,2533,2598,2601,2604,2638,2809,2947,2967,3000,3037,3050,3057,3128,3200,3217,3273,3299,3306,3311,3312,3389,3460,3500,3628,3632,3690,3780,3790,3817,4000,4322,4433,4444-4445,4659,4679,4848,5000,5038,5040,5051,5060-5061,5093,5168,5247,5250,5351,5353,5355,5400,5405,5432-5433,5498,5520-5521,5554-5555,5560,5580,5601,5631-5632,5666,5800,5814,5900-5910,5920,5984-5986,6000,6050,6060,6070,6080,6082,6101,6106,6112,6262,6379,6405,6502-6504,6542,6660-6661,6667,6905,6988,7001,7021,7071,7080,7144,7181,7210,7443,7510,7579-7580,7700,7770,7777-7778,7787,7800-7801,7879,7902,8000-8001,8008,8014,8020,8023,8028,8030,8080-8082,8087,8090,8095,8161,8180,8205,8222,8300,8303,8333,8400,8443-8444,8503,8800,8812,8834,8880,8888-8890,8899,8901-8903,9000,9002,9060,9080-9081,9084,9090,9099-9100,9111,9152,9200,9390-9391,9443,9495,9809-9815,9855,9999-10001,10008,10050-10051,10080,10098,10162,10202-10203,10443,10616,10628,11000,11099,11211,11234,11333,12174,12203,12221,12345,12397,12401,13364,13500,13838,14330,15200,16102,17185,17200,18881,19300,19810,20010,20031,20034,20101,20111,20171,20222,22222,23472,23791,23943,25000,25025,26000,26122,27000,27017,27888,28222,28784,30000,30718,31001,31099,32764,32913,34205,34443,37718,38080,38292,40007,41025,41080,41523-41524,44334,44818,45230,46823-46824,47001-47002,48899,49152,50000-50004,50013,50500-50504,52302,55553,57772,62078,62514,65535";
const portType5Content =
  "21,22,23,25,80,81,82,83,84,88,137,143,443,445,554,631,1080,1883,1900,2000,2323,U:3671,U:3702,4433,4443,4567,5222,5683,7474,7547,8000,8023,8080,8081,8443,8088,U:8600,8883,8888,9000,9090,9999,10000,U:30718,U:37020,37777,U:37810,49152";
const portType6Content =
  "7,11,13,15,17,19,20,21,22,23,25,26,30,31,32,36,37,38,43,49,51,U:53,53,U:67,67,U:69,70,79,U:80,80,81,82,83,84,85,86,87,U:88,88,89,98,102,104,106,110,U:111,111,113,U:113,119,121,U:123,131,135,U:137,138,139,143,U:161,U:162,175,U:177,179,199,211,221,222,264,280,311,389,U:391,U:427,443,U:443,444,445,449,465,U:500,500,502,503,505,512,515,U:520,U:523,540,548,554,564,587,620,U:623,U:626,631,636,646,666,U:705,771,777,789,800,801,808,U:853,873,876,880,888,898,900,901,902,990,992,993,994,995,999,1000,1010,1022,1023,1024,1025,1026,1027,U:1027,1028,1029,1030,1042,1080,1099,1177,U:1194,1194,1200,1201,1212,1214,1234,1241,1248,1260,1290,1302,1311,1314,1344,1389,1400,1433,U:1434,1443,1471,1494,1503,1505,U:1505,1515,1521,1554,1588,U:1604,1610,U:1645,1688,U:1701,1720,1723,1741,1777,1801,U:1812,1830,1863,1880,1883,1900,U:1900,1901,1911,1935,1947,1962,1967,1991,U:1993,2000,2001,2002,2010,2020,2022,2024,2030,2049,2051,2052,2053,2055,2064,2077,2080,2082,2083,U:2083,2086,2087,U:2094,2095,2096,2103,2105,2107,2121,U:2123,U:2152,2154,2160,2181,2222,2223,2252,2306,2323,2332,U:2362,2375,2376,2379,2396,2401,2404,2406,U:2424,2424,U:2425,U:2427,2443,2455,2480,2501,2525,2600,2601,2604,2628,U:2638,2701,2715,2809,2869,3000,3001,3002,3005,3050,3052,3075,3097,3128,3260,3280,U:3283,3288,3299,3306,3307,3310,3311,3312,U:3333,3333,3337,3352,3372,3388,3389,3390,U:3391,3443,3460,U:3478,3520,3522,3523,3524,3525,3528,3531,3541,3542,3567,U:3671,3689,3690,U:3702,3749,3780,U:3784,3790,4000,4022,4040,U:4050,4063,4064,U:4070,4155,4190,4200,4300,4369,4430,4433,4440,4443,4444,U:4500,4505,4506,4567,4660,4664,4711,4712,4730,4782,4786,U:4800,4840,4842,4848,4880,4911,4949,5000,U:5000,U:5001,5001,U:5002,5002,5003,5004,U:5004,5005,U:5005,U:5006,5006,5007,U:5007,5008,U:5008,5009,5010,5038,U:5050,5050,5051,5060,U:5060,U:5061,5061,5080,5084,U:5093,U:5094,U:5095,5111,5222,5236,5258,5269,5280,U:5351,U:5353,5357,5400,U:5405,5427,5432,5443,5550,U:5554,5555,5560,5577,5598,5631,U:5632,5672,U:5673,5678,U:5683,5701,5800,5801,5802,5820,5873,5900,5901,5902,5903,5938,5984,5985,5986,6000,6001,U:6002,6002,U:6003,6003,6004,6005,6006,U:6006,6007,6008,6009,6010,6060,U:6060,6068,6080,6082,6103,6346,6363,6379,6443,6488,U:6502,6544,6560,6565,6581,6588,6590,6600,6664,6665,6666,6667,6668,6669,6697,6699,6780,6782,6868,U:6881,U:6969,6998,7000,U:7000,7001,U:7001,7002,7003,U:7003,7004,7005,U:7005,7007,7010,7014,7070,7071,7077,7080,7100,7144,7145,7170,7171,7180,7187,7199,7272,7288,7382,7401,7402,7443,7474,7479,7493,7500,7537,7547,7548,7634,7657,7676,7776,7777,7778,7779,7780,7788,7911,8000,8001,8002,U:8002,8003,8004,8005,8006,8007,8008,8009,8010,8020,8025,8030,8032,8040,8058,8060,8069,8080,8081,8082,8083,8084,8085,8086,8087,8088,8089,8090,8091,8092,8093,8094,8095,8096,8097,8098,8099,8111,8112,8118,8123,8125,8126,8129,8138,8139,8140,8159,8161,8181,8182,8194,8200,8222,8291,8332,8333,8334,8351,8377,8378,8388,8443,8444,8480,8500,8529,8545,8546,8554,8567,U:8600,8649,8686,8688,8728,8729,8765,8800,8834,8848,8880,8881,8882,8883,8884,8885,8886,8887,8888,U:8888,8889,8890,8899,8983,8999,9000,U:9000,9001,9002,9003,9004,9005,9006,9007,9008,9009,9010,U:9011,9012,9030,9042,9050,9051,9080,9083,9090,9091,9092,9093,9100,U:9100,9108,9151,9160,9191,9200,9229,9292,9295,9300,9306,9333,9334,9418,9443,9444,9446,9527,9530,9595,U:9600,9653,9668,9700,9711,9801,9864,9869,9870,9876,9943,9944,9981,9997,9999,10000,U:10000,10001,U:10001,10003,10005,10030,10035,10162,10243,10250,10255,10332,10333,10389,10443,10554,10909,10911,10912,11001,11211,U:11211,11300,11310,11371,11965,12000,12300,12345,12999,13579,13666,13720,13722,14000,14147,14265,14443,14534,15000,16000,16010,16030,16922,16923,16992,16993,17000,U:17185,17988,18000,18001,18080,18081,18086,18245,18246,18264,19150,19888,19999,20000,U:20000,20002,20005,20201,20202,20332,20547,20880,22105,22222,22335,23023,23424,25000,25010,25105,25565,26214,26257,26470,27015,U:27015,27016,27017,28015,28017,28080,U:28784,29876,29999,30001,30005,U:30310,U:30311,U:30312,U:30313,U:30718,31337,32400,U:32412,U:32414,U:32768,32769,32770,32771,32773,33338,U:33848,33890,34567,34599,U:34962,U:34963,U:34964,U:37020,37215,37777,U:37810,40000,40001,41795,42873,44158,44818,U:44818,45554,U:47808,U:48899,49151,49152,49153,49154,49155,49156,49157,49158,49159,49160,49161,49163,49165,49167,49664,49665,49666,49667,49668,49669,49670,49671,49672,49673,49674,50000,50050,50060,50070,50075,50090,50100,50111,51106,52869,U:53413,54321,55442,55553,55555,U:59110,60001,60010,60030,60443,61222,61613,61616,62078,U:64738,64738";
const portType7Content = "0-65535";
const portTypeConent = ref(portType1Conent);
watch(
  () => portType.value,
  val => {
    switch (val) {
      case "portType1":
        portTypeConent.value = portType1Conent;
        break;
      case "portType2":
        portTypeConent.value = portType2Content;
        break;
      case "portType3":
        portTypeConent.value = portType3Content;
        break;
      case "portType4":
        portTypeConent.value = portType4Content;
        break;
      case "portType5":
        portTypeConent.value = portType5Content;
        break;
      case "portType6":
        portTypeConent.value = portType6Content;
        break;
      case "portType7":
        portTypeConent.value = portType7Content;
        break;
    }
  }
);

const vulScanType = ref("-1");

function runPlugin() {
  let assetId = -1;
  if (region.value == "asset_selected") {
    assetId = currentTarget.value.id;
  } else {
    assetId = -2;
  }
  const scanConfig = {
    portTypeConent: portTypeConent.value,
    vulScanType: vulScanType.value,
    scanRate: scanRate.value
  };
  runPluginApi({
    tagId: p.openInfo.tag_id,
    pluginName: pluginName,
    assetId: assetId,
    config: scanConfig
  }).then(res => {
    ElMessage.success(res.msg);
    gobyopenStatus.value = false;
  });
}
</script>

<template>
  <div>
    <el-dialog
      v-model="gobyopenStatus"
      :title="pluginInfo.pluginName"
      width="40%"
      align-center
      style="border-radius: 12px"
    >
      <el-descriptions
        class="margin-top"
        title="插件信息"
        :column="2"
        size="small"
        border
      >
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">插件名</div>
          </template>
          {{ pluginInfo.pluginName }}
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">目标</div>
          </template>
          <el-tag
            v-for="item in pluginInfo.scanTargetType"
            :key="item"
            style="margin-right: 5px"
          >
            {{ item }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">涉及列</div>
          </template>
          <!-- span v-for 遍历pluginInfo.columnDict -->
          <el-tag
            v-for="(value, key) in pluginInfo.columnDict"
            :key="key"
            style="margin-right: 10px"
          >
            {{ value }}:{{ key }}</el-tag
          >
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">版本</div>
          </template>
          <span size="small">{{ pluginInfo.version }}</span>
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">简介</div>
          </template>
          <span size="small">{{ pluginInfo.description }}</span>
        </el-descriptions-item>
      </el-descriptions>
      <el-descriptions
        class="margin-top"
        title="扫描配置"
        :column="2"
        size="small"
        style="margin-top: 15px"
        border
      />
      <el-form>
        <el-form-item label="扫描目标">
          <el-select v-model="region" placeholder="please select">
            <el-option
              :label="currentTarget.asset_name"
              value="asset_selected"
            />
            <el-option label="所有资产" value="asset_all" />
          </el-select>
        </el-form-item>
        <el-form-item label="扫描端口">
          <el-select v-model="portType" placeholder="端口">
            <el-option label="企业" value="portType1" />
            <el-option label="精简" value="portType2" />
            <el-option label="数据库" value="portType3" />
            <el-option label="常用" value="portType4" />
            <el-option label="物联网" value="portType5" />
            <el-option label="默认" value="portType6" />
            <el-option label="全部" value="portType7" />
          </el-select>
          <el-input
            style="margin-top: 5px"
            placeholder="请输入端口"
            type="textarea"
            :rows="5"
            v-model="portTypeConent"
          />
        </el-form-item>
        <el-row>
          <el-col :span="11">
            <el-form-item label="漏洞选项">
              <el-select v-model="vulScanType" placeholder="please select">
                <el-option label="通用POC" value="0" />
                <el-option label="暴力破解" value="1" />
                <el-option label="全部漏洞" value="2" />
                <el-option label="禁用" value="-1" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="13">
            <el-form-item label="扫描速率">
              <el-input-number v-model="scanRate" :min="1" :max="5000" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <el-button
        type="primary"
        @click="runPlugin"
        round
        style="margin-left: 90%"
        >开始</el-button
      >
    </el-dialog>
  </div>
</template>
<style scoped>
.slider-demo-block {
  display: flex;
  align-items: center;
}
.slider-demo-block .el-slider {
  margin-top: 0;
  margin-left: 12px;
}
.slider-demo-block .demonstration {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  line-height: 44px;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-bottom: 0;
}
.slider-demo-block .demonstration + .el-slider {
  flex: 0 0 70%;
}
</style>

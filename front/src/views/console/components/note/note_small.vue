<script setup lang="ts">
import EditorJS from "@editorjs/editorjs";
import Header from "@editorjs/header";
import { watch, ref } from "vue";
import { Close } from "@element-plus/icons-vue";
import { useNoteStore } from "@/store/modules/note";
import { storeToRefs } from "pinia";
import SimpleImage from "@editorjs/simple-image";
import Paragraph from "@editorjs/paragraph";
import Table from "@editorjs/table";
import Marker from "@editorjs/marker";
import InlineCode from "@editorjs/inline-code";
import Underline from "@editorjs/underline";
import List from "@editorjs/list";
import Checklist from "@editorjs/checklist";
import CodeBox from "@bomdi/codebox";
import { saveNoteApi, openNoteApi } from "@/api/note";
import { getConfig } from "@/config";
import { json } from "stream/consumers";
const { currentAssetIDForNote, currentAssetNameForNote } = storeToRefs(
  useNoteStore()
);

const serverHost = getConfig().serverHost;
const currentNoteId = ref(-1);
let defaultContent;
let socket: WebSocket;
let editor: EditorJS;
watch(
  () => currentAssetIDForNote.value,
  (newVal, oldVal) => {
    if (newVal !== oldVal) {
      if (newVal === -1) {
        editor.destroy();
      } else {
        openNoteApi({ assetId: currentAssetIDForNote.value })
          .then(res => {
            console.log(res);
            defaultContent = JSON.parse(res.data.content);
            console.log(defaultContent);
            currentNoteId.value = res.data.noteId;
            // socket = new WebSocket("ws://" + serverHost + "/note/syncNote");
          })
          .then(() => {
            editor = new EditorJS({
              holder: "editorjs",
              autofocus: true,
              data: defaultContent,
              onChange: (api, event) => {
                api.saver.save().then(outputData => {
                  console.log(outputData);
                });
                console.log("change");
                // socket.send(JSON.stringify({ noteId: currentNoteId.value }));
              },
              tools: {
                header: {
                  class: Header,
                  config: {
                    placeholder: "Header"
                  }
                },
                image: {
                  class: SimpleImage,
                  inlineToolbar: true
                },
                paragraph: {
                  class: Paragraph,
                  inlineToolbar: true
                },
                codeBox: {
                  class: CodeBox,
                  config: {
                    themeURL:
                      "https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@9.18.1/build/styles/dracula.min.css", // Optional
                    themeName: "atom-one-dark", // Optional
                    useDefaultTheme: "light" // Optional. This also determines the background color of the language select drop-down
                  }
                },
                table: {
                  class: Table,
                  inlineToolbar: true,
                  config: {
                    rows: 2,
                    cols: 3
                  }
                },
                Marker: {
                  class: Marker,
                  shortcut: "CMD+SHIFT+M"
                },
                inlineCode: {
                  class: InlineCode
                },
                underline: Underline,
                list: {
                  class: List,
                  inlineToolbar: true,
                  config: {
                    defaultStyle: "unordered"
                  }
                },
                checklist: {
                  class: Checklist,
                  inlineToolbar: true
                }
              }
            });
          });
      }
    }
  }
);

function saveAndExit() {
  editor.saver.save().then(outputData => {
    console.log(outputData);
    saveNoteApi({
      noteId: currentNoteId.value,
      content: outputData
    })
      .then(res => {
        currentAssetIDForNote.value = -1;
        currentNoteId.value = -1;
        console.log(res);
      })
      .catch(err => {
        console.log(err);
        currentNoteId.value = -1;
      });
  });
}

// setInterval(getNewContent, 1000);
</script>

<template>
  <div v-if="currentAssetIDForNote != -1">
    <el-card class="note-card">
      <div class="header-note" style="display: flex">
        <div style="margin-top: -8px">
          <span style="font-size: 12px; color: rgb(126, 126, 126)"
            >选中资产:{{ currentAssetNameForNote }}</span
          >
        </div>
        <el-icon class="note-close" @click="saveAndExit"
          ><Close class="closenoteico"
        /></el-icon>
      </div>
      <el-scrollbar height="540px">
        <div id="editorjs" />
      </el-scrollbar>
    </el-card>
  </div>
</template>
<style>
/* note-card 居中出现在屏幕中间 */
.note-card {
  padding-left: 20px;
  padding-right: 20px;
  padding-top: 10px;
  width: 860px;
  height: 570px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  border-radius: 20px;
  z-index: 9998;
}
#editorjs {
  z-index: 9999;
}
/* note-close右对齐 */
.note-close {
  float: right;
  margin-left: 650px;
  margin-right: 5px;
  cursor: pointer;
}
.header-note {
  height: 20px;
}
.note-close:hover {
  filter: drop-shadow(0em 0em 1.3em #79bbff);
  z-index: 9999;
}

.ce-block__content,
.ce-toolbar__content {
  max-width: 650px;
  font-size: 14px;
}
</style>

<script setup lang="ts">
import EditorJS from "@editorjs/editorjs";
import Header from "@editorjs/header";
import SimpleImage from "@editorjs/simple-image";
import Paragraph from "@editorjs/paragraph";
import CodeBox from "@bomdi/codebox";
import Table from "@editorjs/table";
import Marker from "@editorjs/marker";
import InlineCode from "@editorjs/inline-code";
import Underline from "@editorjs/underline";
import List from "@editorjs/list";
import Checklist from "@editorjs/checklist";
const editor = new EditorJS({
  holder: "editorjs",
  autofocus: true,
  /**
   * Tools list
   */
  onChange: async (api, event) => {
    console.log("现在我知道编辑器的内容发生了变化！", event);
    console.log(typeof event);

    // 检查event是否是一个数组
    if (Array.isArray(event)) {
      // 如果是，遍历数组并处理每个事件
      for (let i = 0; i < event.length; i++) {
        const action = event[i].type;
        const blockIndex = event[i].detail.index;
        const blockAPI = api.blocks.getBlockByIndex(blockIndex);
        const blockData = await blockAPI.save();
        console.log({ action: action, block: blockData });
      }
    } else {
      // 如果不是，像之前一样处理事件
      
      const blockIndex = event.detail.index;
      const blockAPI = api.blocks.getBlockByIndex(blockIndex);
      const blockData = await blockAPI.save();
      console.log("改变的区块的内容是：", blockData);
    }
  },
  tools: {
    header: {
      class: Header,
      inlineToolbar: ["marker", "link"],
      config: {
        placeholder: "Header"
      },
      shortcut: "CMD+SHIFT+H"
    },
    image: {
      class: SimpleImage,
      inlineToolbar: true
    },
    paragraph: {
      class: Paragraph,
      inlineToolbar: true
    },
    code: CodeBox,
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

function svaee() {
  editor.save().then(data => {
    console.log(data);
  });
}

// setInterval(() => {
//   svaee();
// }, 5000);
</script>
<template>
  <div class="test">
    <div id="editorjs" />
  </div>
</template>

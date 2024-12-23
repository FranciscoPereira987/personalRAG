
<script setup>
import { retrieveChatHistory } from '@/commons/calls';
import ChatCore from '@/components/ChatCore.vue';
import ChatOptions from '@/components/ChatOptions.vue';
import { ref } from 'vue';

const store = ref("")
const chat = ref("")
const chatHistory = ref([])

const updateHistory = async () => {
  if (chat.value == "") {
    chatHistory.value = []
  }else {
    chatHistory.value = await retrieveChatHistory(chat.value)
  }
}
</script>

<template>
  <div style="display: flex; height: 100%; min-width: 100%;">
    <ChatOptions v-model:store="store" v-model:chat="chat" @update:chat="updateHistory"/>
    <ChatCore 
      v-model:chat="chat" 
      v-model:store="store"
      v-model:chat-history="chatHistory"/>
  </div>
</template>


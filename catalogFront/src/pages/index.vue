
<script setup>
import ChatCore from '@/components/ChatCore.vue';
import ChatOptions from '@/components/ChatOptions.vue';
import { ref } from 'vue';

const store = ref("")
const chat = ref("")

</script>

<template>
  <div style="display: flex; height: 100%; min-width: 100%;">
    <ChatOptions v-model:store="store" v-model:chat="chat"/>
    <ChatCore v-model:chat="chat" v-model:store="store"/>
    <div>
      <p>{{ store }}</p>
      <p>{{ chat }}</p>
    </div>
  </div>
</template>



<script setup>
import ChatCore from '@/components/ChatCore.vue';
import ChatOptions from '@/components/ChatOptions.vue';
import { ref } from 'vue';

const store = ref("No Store Selected")
const chat = ref("No chat Selected")

</script>

<template>
  <div style="display: flex; height: 100%; min-width: 100%;">
    <ChatOptions v-model:store="store" v-model:chat="chat"/>
    <ChatCore />
    <div>
      <p>{{ store }}</p>
      <p>{{ chat }}</p>
    </div>
  </div>
</template>


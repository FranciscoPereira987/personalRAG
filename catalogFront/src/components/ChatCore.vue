<script setup>
import { postCompletion } from '@/commons/calls';
import { ref } from 'vue';
import { marked } from 'marked';
const store = "prueba"
const chat = ref('')
const input = ref('') 
const printClick = async () => {
   if (input.value != ''){
       chatPlaceHolder.value.push(
            {"role": "user", "content": input.value})
        let response = await postCompletion(chat.value == '' ? null : chat.value, store, input.value)
        if (chat.value == '') {
            chat.value = response.id
        }
        console.log(chat.value)
        chatPlaceHolder.value.push(
            response.choices[0].message
        )
       input.value = '' 
   }
}

const chatPlaceHolder = ref([])

</script>

<template>
   <div v-for="message in chatPlaceHolder">
    <v-text-field disabled=true :prepend-icon="message.role == 'assistant' ? 'mdi-chat' : 'mdi-chat-outline'">
        <div v-html="marked(message.content)"></div>
    </v-text-field>
   </div> 
    <v-text-field 
        label="New Message" 
        prepend-icon="mdi-chat-plus-outline" 
        append-icon="mdi-send" 
        v-model="input"
        @click:append="printClick">
    </v-text-field>
</template>
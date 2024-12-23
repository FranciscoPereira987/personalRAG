<script setup>
import { postCompletion } from '@/commons/calls';
import { ref } from 'vue';
import { marked } from 'marked';
const store = defineModel("store")
const chat = defineModel("chat") 
const input = ref('') 
const chatPlaceHolder = defineModel("chat-history")

const printClick = async () => {
   if (input.value != ''){
       chatPlaceHolder.value.push(
            {"role": "user", "content": input.value})
        let response = await postCompletion(chat.value == '' ? null : chat.value, store.value, input.value)
        if (chat.value == '') {
            chat.value = response.id
        }
        chatPlaceHolder.value.push(
            response.choices[0].message
        )
       input.value = '' 
   }
}

</script>

<template>
    <div class="main-chat-core-div">
            <div v-for="message in chatPlaceHolder">
                <v-text-field disabled=true :prepend-icon="message.role == 'assistant' ? 'mdi-robot-outline' : 'mdi-chat-outline'">
                    <div v-html="marked(message.content)"></div>
                </v-text-field>
            </div>  
        <v-text-field
            class="new-message" 
            label="New Message" 
            prepend-icon="mdi-chat-plus-outline" 
            append-icon="mdi-send" 
            v-model="input"
            @click:append="printClick">
        </v-text-field>
    </div>
</template>


<style>
    .main-chat-core-div {
        display: flex;
        flex: 1;
        flex-direction: column;
        height: 100%;
        margin-left: 2%
    }
    .new-message {
        max-height: 10%;
        margin-top: auto;
    }
</style>
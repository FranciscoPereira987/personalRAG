<script setup>
import { postCompletion } from '@/commons/calls';
import { ref } from 'vue';
import { marked } from 'marked';
const store = defineModel("store")
const chat = defineModel("chat") 
const input = ref('') 
const chatPlaceHolder = defineModel("chat-history")
const loading = ref(false)
const chatError = ref(false)

const sendChatMessage = async () => {
    if (chat.value == "") {
        chatError.value = true        
        return
    }
    if (input.value != ''){
        loading.value = true
        chatPlaceHolder.value.push(
            {"role": "user", "content": input.value})
        let request = postCompletion(chat.value == '' ? null : chat.value, store.value, input.value)
        input.value = ''
        let response = await request
        if (chat.value == '') {
            chat.value = response.id
        }
        chatPlaceHolder.value.push(
            response.choices[0].message
        )
   }
   loading.value = false 
}
</script>

<template>
    <div class="main-chat-core-div">
            <div v-for="message in chatPlaceHolder">
                <v-text-field :disabled="true" :prepend-icon="message.role == 'assistant' ? 'mdi-robot-outline' : 'mdi-chat-outline'">
                    <div v-html="marked(message.content)"></div>
                </v-text-field>
            </div>  
        <v-text-field
            class="new-message" 
            :label="chatError ? 'No chat' : 'New Message'"
            :loading="loading" 
            :error="chatError"
            prepend-icon="mdi-chat-plus-outline" 
            append-icon="mdi-send" 
            v-model="input"
            @keydown.enter="sendChatMessage"
            @click:append="sendChatMessage">
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
        position: sticky;
        bottom: 0px;
    }
</style>
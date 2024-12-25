<script setup>
import { createNewChat } from '@/commons/calls';
import { ref } from 'vue';


const isActive = defineModel("active")
const currentChat = defineModel("chat")
const newChatName = ref('')
const loading = ref(false)
const nameError = ref(false)

const createChat = async () => {
    if (newChatName.value == '') {
        nameError.value = true
        return
    } 
    loading.value = true
    await createNewChat(newChatName.value)
    currentChat.value = newChatName.value
    loading.value = false
    newChatName.value = ''
    isActive.value = false
}

</script>

<template>
<v-dialog
        v-model="isActive"
        width="auto">
        <v-card
            :loading="loading"
            class="main-card"
            title="New Chat">
            <template v-slot:default>
                <v-text-field
                    class="input-field"
                    label="Chat Name"
                    :error="nameError"
                    v-model="newChatName"
                    @keydown.enter="createChat">
                </v-text-field>
            </template>
            <template v-slot:actions>
                <v-btn
                    text="Cancel"
                    @click="isActive = false"
                    >
                </v-btn>
                <v-btn
                    text="Create"
                    @click="createChat">
                </v-btn>
            </template>
        </v-card> 
    </v-dialog>
</template>
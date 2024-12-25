<script setup>
import { onMounted, ref } from 'vue';
import StoreCreation from './StoreCreation.vue';
import ChatCreation from './ChatCreation.vue';
import { getAvailableChats, getAvailableStores } from '@/commons/calls';
import StoreUpdate from './StoreUpdate.vue';

const storeNames = ref([])
const chatNames = ref([])
const storeCreationActive = ref(false)
const newChatCreationActive = ref(false)
const storeUpdateActive = ref(false)
const selected = defineModel("store")
const chat = defineModel("chat")

let loadStores = async () => {
    let stores = await getAvailableStores()
    let chats  = await getAvailableChats()
    storeNames.value = stores
    chatNames.value = chats
}

onMounted(loadStores)

let resetChat = async () => {
    chat.value = ""
    newChatCreationActive.value = true
    await loadStores()
}

</script>
<!-- 
    Here should go the options to select the:
        1. Paths that the user would like to store
        2. The posibility to select the store where to put this embeddings 
-->
<template>
    <v-card class='main-div' variant="tonal">
        <template v-slot:default>
                <v-select 
                class="menu-element"
                variant="outlined"
                label="Chat"
                :items="chatNames"
                v-model="chat"
                >
            </v-select>
            <v-select
                class="menu-element"
                variant="outlined"
                label="Store"
                :items="storeNames"
                v-model="selected"
                >
            </v-select>
            <v-btn
                class="create-btn" 
                v-if="selected != ''"
                @click="storeUpdateActive = true"
                >
                Update Store
            </v-btn>
            <v-btn 
                class="create-btn last-btn" 
                variant="tonal" 
                @click="resetChat">
                New Chat
            </v-btn>
            <v-btn 
                class="create-btn not-last-btn" 
                variant="tonal" 
                @click="storeCreationActive = true">
                New Store
            </v-btn>
        </template>
    </v-card>
    <ChatCreation 
        v-model:active="newChatCreationActive" 
        v-model:chat="chat"/>
    <StoreCreation 
        v-model:active="storeCreationActive"/>
    <StoreUpdate 
        v-model:active="storeUpdateActive" 
        :store="selected"/>
</template>

<style>
    .main-div {
        display: flex;
        flex-direction: column;
        position: sticky;
        top: 0px;
        width: 20%;
        height: 100vh;
    }
    .menu-element {
        max-height: 10%;
        margin-top: 2%;
        margin-left: 1%;
        margin-right: 1%;
    }
    .create-btn {
        width: 98%;
        margin-bottom: 2%;
        margin-left: 1%;
        margin-right: 1%; 
    }
    .last-btn {
        margin-top: auto;
    }
    .not-last-btn {
        margin-top: 2%;
    }
</style>
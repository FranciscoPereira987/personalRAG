<script setup>
import { ref } from 'vue';

const storeNames = ref(["A", "B", "C", "D"])
const chatNames = ref(["Chat-A", "Chat-B", "Chat-C", "Chat-D"])
const selected = defineModel("store")
const chat = defineModel("chat")

</script>
<!-- 
    Here should go the options to select the:
        1. Paths that the user would like to store
        2. The posibility to select the store where to put this embeddings 
-->
<template>
    <v-card class='main-div' variant="tonal">
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
        <v-btn class="create-btn" variant="tonal">
            New Chat
        </v-btn>
        <v-btn class="create-btn" variant="tonal">
            New Store
        </v-btn>
    </v-card>
</template>

<style>
    .main-div {
        display: flex;
        flex-direction: column;
        width: 20%;
        height: 100vh;
    }
    .menu-element {
        margin-top: 2%;
        margin-left: 1%;
        margin-right: 1%;
    }
    .create-btn {
         
        width: 98%;
        margin-bottom: 2%;
        margin-top: 2%;
        margin-left: 1%;
        margin-right: 1%; 
    }
</style>
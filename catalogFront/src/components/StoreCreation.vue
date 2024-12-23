<script setup>
import { ref } from 'vue';
const isActive = defineModel("active")
const storeName = ref('')
const storePath = ref('')
const isFile = ref(false)
const logInfo = () => {
 
}
</script>

<template>
    <v-dialog
        v-model="isActive"
        width="auto">
        <v-card
            class="main-card"
            title="New Store">
            <template v-slot:default>
                <v-text-field
                    class="input-field"
                    label="Store Name"
                    v-model="storeName">
                </v-text-field>
                <v-file-input
                    class="input-field" 
                    v-if="isFile" 
                    label="File upload"></v-file-input>
                <v-text-field
                    v-else
                    class="input-field"
                    label="Path Name"
                    v-model="storePath">
                </v-text-field>
                <v-switch
                    label="Upload file"
                    v-model="isFile">
                </v-switch> 
            </template>
            <template v-slot:actions>
                <v-btn
                    text="Cancel"
                    @click="isActive = false"
                    >
                </v-btn>
                <v-btn
                    text="Create"
                    @click="logInfo">
                </v-btn>
            </template>
        </v-card> 
    </v-dialog>
</template>

<style>
    .main-card {
        display: flex;
        align-items: center;
        min-width: 70vb;
    }
    .input-field {
        width: 90%;
    }
</style>
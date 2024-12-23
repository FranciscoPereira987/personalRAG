<script setup>
import { newStoreWithPath } from '@/commons/calls';
import { ref } from 'vue';
const isActive = defineModel("active")
const storeName = ref('')
const storePath = ref('')
const isFile = ref(false)

const nameError = ref(false)
const pathError = ref(false)

const loading = ref(false)

const restartValues = () => {
    storeName.value = ''
    storePath.value = ''
    loading.value = false
    isActive = false
}

const createStore = async () => {
    nameError.value = false
    pathError.value = false
    if (storeName.value == '' || storePath.value == '') {
        nameError.value = storeName.value == ''
        pathError.value = storePath.value == ''
        return
    }
    loading.value = true
    await newStoreWithPath(storeName.value, storePath.value)
    restartValues()
}
</script>

<template>
    <v-dialog
        v-model="isActive"
        width="auto">
        <v-card
            :loading="loading"
            class="main-card"
            title="New Store">
            <template v-slot:default>
                <v-text-field
                    class="input-field"
                    label="Store Name"
                    :error="nameError"
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
                    :error="pathError"
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
                    @click="createStore">
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
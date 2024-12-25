<script setup>
import { updateStoreWithDir } from '@/commons/calls';
import { ref } from 'vue';

const isActive = defineModel("active")
const isFile = ref(false)
const loading = ref(false)
const dir = ref("")
const nameError = ref(false)
const props = defineProps(["store"])


const updateDirectory = async () => {
    nameError.value = dir.value == ""
    if (dir.value == "") {
        return    
    }
    loading.value = true
    await updateStoreWithDir(props.store, dir.value)
    nameError.value = false
    loading.value = false
    dir.value = ""
}

const updateFile = async () => {

}

</script>

<template>
    <v-dialog
        v-model="isActive"
        width="auto">
        <v-card
            :loading="loading"
            class="main-card"
            title="Update Store">
            <template v-slot:default>
                <v-file-input
                    class="input-field" 
                    v-if="isFile" 
                    label="File upload"></v-file-input>
                <v-text-field
                    v-else
                    class="input-field"
                    label="Path Name"
                    :error="nameError"
                    v-model="dir"
                    @keydown.enter="updateDirectory">
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
                    text="Add to store"
                    @click="updateDirectory"
                    >
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
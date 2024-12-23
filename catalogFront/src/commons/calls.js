import ChatHistory from "@/components/ChatHistory.vue"
import axios from "axios"

const API_URL = "http://127.0.0.1:8000"
const API_CHAT_COMPLETION = "/completion"
const API_CHAT_HISTORY = "/chats"
const API_AVAILABLE_STORES = "/stores"

function ChatData(chat, store, input) {
    let basicData = {
        "input": input
    }
    if (store != null) {
        basicData.store = store
    }
    if (chat != null) {
        basicData.chat_id = chat
    }
    return basicData 
}


export async function postCompletion(chat, store, input) {
    let endpoint = API_URL + API_CHAT_COMPLETION
    let response = await axios.post(endpoint, ChatData(chat, store, input))
    return await response.data 
}

export async function getAvailableStores() {
    let endpoint = API_URL + API_AVAILABLE_STORES
    let response = await axios.get(endpoint)
    return await response.data
}

export async function getAvailableChats() {
    let endpoint = API_URL + API_CHAT_HISTORY
    let response = await axios.get(endpoint)
    return await response.data
}
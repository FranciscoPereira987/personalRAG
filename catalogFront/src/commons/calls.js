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
    console.log(basicData)
    return basicData 
}

//Sends a new message
export async function postCompletion(chat, store, input) {
    let endpoint = API_URL + API_CHAT_COMPLETION
    let response = await axios.post(endpoint, ChatData(chat, store, input))
    return await response.data 
}
//Returns the available stores for the RAG chat
export async function getAvailableStores() {
    let endpoint = API_URL + API_AVAILABLE_STORES
    let response = await axios.get(endpoint)
    return await response.data
}
//Creates a new store with a given path
export async function newStoreWithPath(name, path) {
    const data = {
        "store_name": name,
        "store_path": path 
    }
    let endpoint = API_URL + API_AVAILABLE_STORES
    let response = await axios.post(endpoint, data)
    return await response.data 
}
//Returns the messages associated with the given chat
export async function retrieveChatHistory(chat) {
   let endpoint = API_URL + API_CHAT_HISTORY + "/" + chat
   let response = await axios.get(endpoint)
   return await response.data
}
//Returns the available chats
export async function getAvailableChats() {
    let endpoint = API_URL + API_CHAT_HISTORY
    let response = await axios.get(endpoint)
    return await response.data
}
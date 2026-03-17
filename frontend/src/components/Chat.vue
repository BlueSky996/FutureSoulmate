<script setup>
import { ref } from "vue"

const message = ref("")
const messages = ref([])

const sessionId = ref(null)
const wife = ref(null)

const API = "http://localhost:8000"

async function start() {
    const res = await fetch(API + "/generate-wife", { method:"POST"})
    wife.value = await res.json()

}

async function sendMessage() {

    if(!message.value) return

    messages.value.push({type:"user", text:message.value})

    const res = await fetch(API + "/chat", {
        method:"POST",
        headers: { "Content-Type":"application/json"},
        body: JSON.stringify({
            message: message.value,
            session_id: sessionId.value,
            wife: wife.value
        })
        })
    
    const data = await res.json()
    sessionId.value = data.session_id

    messages.value.push(data)
    message.value = ""
}

</script>

<template>
<div class="chat">

    <button v-if="!wife" @click="start()">Start Chat</button>

    <div v-for="(msg,i) in messages" :key="i">

        <div v-if="msg.type === 'chat'">
            {{ msg.text }}
        </div>

        <div v-if="msg.type === 'image'">
            {{ msg.text }}
            <img :src="API + msg.image" width="200">
        </div>

        <div v-if="msg.type === 'offer'">
            {{ msg.text }}
            <a :href="msg.link" target="_blank">Join me</a>
        </div>
    </div>

    <input v-model="message">
    <button @click="sendMessage()">Send</button>
</div>

</template>
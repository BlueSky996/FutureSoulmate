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
    console.log("DATA:", data)
    sessionId.value = data.session_id

    messages.value.push({
        type: data.type,  // map reply to type
        text: data.text,
        image: data.image,
        link: data.link
    })
    message.value = ""
}

</script>

<template>
<div class="chat">

    <button v-if="!wife" @click="start()">Start Chat</button>

    <div v-for="(msg,i) in messages" :key="i">

        <div v-if="msg.type === 'user'">
            You: {{ msg.text }}
        </div>

        <div v-else-if="msg.type === 'chat'">
           Wife: {{ msg.text }}
        </div>

        <div v-else-if="msg.type === 'image'">
            <p>{{ msg.text }}</p>
            <img :src="API + msg.image" width="200">
        </div>

        <div v-else-if="msg.type === 'offer'">
            <p>{{ msg.text }}</p>
            <a :href="msg.link" target="_blank">Join me</a>
        </div>

    </div>

    <input v-model="message">
    <button @click="sendMessage()">Send</button>
</div>

</template>
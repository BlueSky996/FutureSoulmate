<script setup>
import { ref } from "vue"

const message = ref("")
const messages = ref([])
const sessionId = ref(null)
const wife = ref(null)


const API = "http://localhost:8000"

async function start(payload = {}) {
    const res = await fetch(API + "/generate-wife", { 
        method:"POST",
        headers: { "Content-Type":"application/json"},
        body: JSON.stringify(payload)
    })
    wife.value = await res.json()
}

async function sendMessage() {

    if(!message.value || !wife.value) return

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
    // keep existing sessionId if backend didn't return one
    sessionId.value = data.session_id || sessionId.value

    // support either type or legacy reply
    messages.value.push({
        type: data.type || data.reply || "chat",  // map reply to type
        text: data.text || "",
        image: data.image,
        link: data.link
    })
    message.value = ""
}
</script>

<template>
<div class="chat">
    <div v-if="!wife" class="start-wrap">
        <button v-if="!wife" @click="start()">Start Chat (random)</button>
    </div>
    
    <!-- chat UI -->
    <div v-else class="chat-wrap">
        <div class="wife-header">
            <img :src="API + wife.image" alt="wife" />
            <div class="wife-info">
                <h3>{{ wife.name }}</h3>
                <p v-if="wife.traits">{{ wife.traits.join(', ') }}</p>
                <p v-if="wife.religion" class="muted">{{ wife.religion }}</p>
            </div>
        </div>

    <div class="messages">
    <div v-for="(msg,i) in messages" :key="i" class="msg-row">

        <div v-if="msg.type === 'user'" class="msg user">
            You: {{ msg.text }}
        </div>

        <div v-else-if="msg.type === 'chat'" class="msg wife">
           Wife: {{ msg.text }}
        </div>

        <div v-else-if="msg.type === 'image'" class="msg wife">
            <p>{{ msg.text }}</p>
            <img :src="API + msg.image" width="200" />
        </div>

        <div v-else-if="msg.type === 'offer'" class="msg offer">
            <p>{{ msg.text }}</p>
            <a :href="msg.link" target="_blank">Join me</a>
        </div>
    </div>
    </div>

    <div class="input-row">
    <input v-model="message" :disabled="!wife" placeholder="Type a message..." /> 
    <button @click="sendMessage()" :disabled="!wife || !message">Send</button>
</div>

</div>
</div>

</template>

<style scoped>
.chat { max-width:720px; margin:0 auto; color:#fff; font-family:Arial, Helvetica, sans-serif; }
.start-wrap { display:flex; justify-content:center; padding:40px 0; }
.wife-header { display:flex; gap:12px; align-items:center; padding:12px; background:#111; border-radius:8px; margin-bottom:12px; }
.wife-header img { width:64px; height:64px; border-radius:50%; object-fit:cover; }
.wife-info h3 { margin:0; }
.wife-info .muted { color:#aaa; font-size:12px; margin:4px 0 0; }
.messages { max-height:60vh; overflow:auto; padding:8px; display:flex; flex-direction:column; gap:8px; }
.msg { padding:10px 12px; border-radius:12px; max-width:70%; }
.msg.user { background:#2b2b42; margin-left:auto; }
.msg.wife { background:#ff4d6d; color:#fff; }
.msg.offer { background:#ff2e63; text-align:center; color:#fff; }
.input-row { display:flex; gap:8px; padding:12px; background:#0f0f14; border-radius:8px; margin-top:8px; }
.input-row input { flex:1; padding:10px; border-radius:8px; border:none; background:#111; color:#fff; }
.input-row button { padding:10px 16px; border:none; border-radius:8px; background:#ff4d6d; color:#fff; cursor:pointer; }
</style>
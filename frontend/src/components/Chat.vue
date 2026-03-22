<script setup>
import { ref } from "vue"
import SoulmateSelector from "./SoulSelector.vue"

const message = ref("")
const messages = ref([])
const sessionId = ref(null)
const props = defineProps(["initialData"])
const soulmate = ref(null)

onMounted(() => {
  soulmate.value = props.initialData
})

const API = "http://localhost:8000"

async function start(payload = {}) {
    const res = await fetch(API + "/generate-soulmate", { 
        method:"POST",
        headers: { "Content-Type":"application/json"},
        body: JSON.stringify(payload)
    })
    soulmate.value = await res.json()
}

async function sendMessage() {

    if(!message.value || !soulmate.value) return

    messages.value.push({type:"user", text:message.value})

    const res = await fetch(API + "/chat", {
        method:"POST",
        headers: { "Content-Type":"application/json"},
        body: JSON.stringify({
            message: message.value,
            session_id: sessionId.value,
            soulmate: soulmate.value
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
    <div v-if="!soulmate" class="start-wrap">
        <button v-if="!soulmate" @click="start()">Start Chat (random)</button>
    </div>
    
    <!-- chat UI -->
    <div v-else class="chat-wrap">
        <div class="soulmate-header">
            <img :src="API + soulmate.image" alt="soulmate" />
            <div class="soulmate-info">
                <h3>{{ soulmate.name }}</h3>
                <p v-if="soulmate.traits">{{ soulmate.traits.join(', ') }}</p>
                <p v-if="soulmate.religion" class="muted">{{ soulmate.religion }}</p>
            </div>
        </div>

    <div class="messages">
    <div v-for="(msg,i) in messages" :key="i" class="msg-row">

        <div v-if="msg.type === 'user'" class="msg user">
            You: {{ msg.text }}
        </div>

        <div v-else-if="msg.type === 'chat'" class="msg soulmate">
           soulmate: {{ msg.text }}
        </div>

        <div v-else-if="msg.type === 'image'" class="msg soulmate">
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
    <input v-model="message" :disabled="!soulmate" placeholder="Type a message..." /> 
    <button @click="sendMessage()" :disabled="!soulmate || !message">Send</button>
</div>

</div>
</div>

</template>

<style scoped>
.chat { max-width:720px; margin:0 auto; color:#fff; font-family:Arial, Helvetica, sans-serif; }
.start-wrap { display:flex; justify-content:center; padding:40px 0; }
.soulmate-header { display:flex; gap:12px; align-items:center; padding:12px; background:#111; border-radius:8px; margin-bottom:12px; }
.soulmate-header img { width:64px; height:64px; border-radius:50%; object-fit:cover; }
.soulmate-info h3 { margin:0; }
.soulmate-info .muted { color:#aaa; font-size:12px; margin:4px 0 0; }
.messages { max-height:60vh; overflow:auto; padding:8px; display:flex; flex-direction:column; gap:8px; }
.msg { padding:10px 12px; border-radius:12px; max-width:70%; }
.msg.user { background:#2b2b42; margin-left:auto; }
.msg.soulmate { background:#ff4d6d; color:#fff; }
.msg.offer { background:#ff2e63; text-align:center; color:#fff; }
.input-row { display:flex; gap:8px; padding:12px; background:#0f0f14; border-radius:8px; margin-top:8px; }
.input-row input { flex:1; padding:10px; border-radius:8px; border:none; background:#111; color:#fff; }
.input-row button { padding:10px 16px; border:none; border-radius:8px; background:#ff4d6d; color:#fff; cursor:pointer; }
</style>
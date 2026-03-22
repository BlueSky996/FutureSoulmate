<script setup>
import { ref } from "vue"

import Chat from "./components/Chat.vue"
import SoulmateSelector from "./components/SoulmateSelector.vue"

const soulmate = ref(null)

//  receive data from selector then pass to Chat
function handleStart(data) {
  soulmate.value = data
}
</script>

<template>
  <!--  show selector first -->
  <SoulmateSelector v-if="!soulmate" @start="handleStart" />

  <!--  pass soulmate to chat -->
  <Chat v-else :initialData="soulmate" />
</template>
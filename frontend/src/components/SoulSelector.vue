<template>
  <div class="setup">
    <h2>Create your Soulmate</h2>

    <label class="field">
      <span>Name</span>
      <select v-model="selectedName">
        <option value="" disabled>Select name (or leave blank)</option>
        <option v-for="n in names" :key="n" :value="n">{{ n }}</option>
      </select>
    </label>

    <label class="field">
      <span>Religion</span>
      <select v-model="selectedReligion">
        <option value="" disabled>Select religion (or leave blank)</option>
        <option v-for="r in religions" :key="r" :value="r">{{ r }}</option>
      </select>
    </label>

    <div class="field">
      <span>Traits (pick 1–4)</span>
      <div class="traits">
        <button
          v-for="t in traits"
          :key="t"
          :class="{ active: selectedTraits.includes(t) }"
          @click="toggleTrait(t)"
          type="button"
        >
          {{ t }}
        </button>
      </div>
    </div>

    <button class="start" @click="start()">Start Chat</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"

const emit = defineEmits(["start"])
const API = "http://localhost:8000"

const names = ref([])
const traits = ref([])
const religions = ref([])

const selectedName = ref("")
const selectedTraits = ref([])
const selectedReligion = ref("")

onMounted(async () => {
  try {
    const res = await fetch(API + "/soulmate-options")
    const data = await res.json()
    names.value = data.names || []
    traits.value = data.traits || []
    religions.value = data.religions || []
  } catch (e) {
    names.value = []
    traits.value = []
    religions.value = []
  }
})

function toggleTrait(t) {
  const idx = selectedTraits.value.indexOf(t)
  if (idx !== -1) {
    selectedTraits.value.splice(idx, 1)
  } else {
    if (selectedTraits.value.length < 4) selectedTraits.value.push(t)
  }
}

function start() {
  emit("start", {
    name: selectedName.value || "",
    traits: selectedTraits.value.slice(),
    religion: selectedReligion.value || ""
  })
}
</script>

<style scoped>
.setup {
  display:flex;
  flex-direction:column;
  gap:12px;
  padding:16px;
  max-width:420px;
  margin:0 auto;
  color:#fff;
  background:linear-gradient(180deg,#0f0f14,#121217);
  border-radius:12px;
}
.field { display:flex; flex-direction:column; gap:6px; }
select { padding:8px 10px; border-radius:8px; border:1px solid #222; background:#0b0b0f; color:#fff; }
.traits { display:flex; flex-wrap:wrap; gap:8px; }
.traits button {
  padding:8px 12px;
  border-radius:12px;
  border:none;
  background:#222;
  color:#fff;
  cursor:pointer;
}
.traits button.active { background:#ff4d6d; color:white; }
.start {
  margin-top:6px;
  padding:10px;
  border-radius:12px;
  border:none;
  background:#ff4d6d;
  color:#fff;
  cursor:pointer;
}
</style>
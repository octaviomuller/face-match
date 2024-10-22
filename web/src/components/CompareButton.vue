<script setup lang="ts">
import { computed, ref } from 'vue'
import { uploadFile } from '@/api'
import { store } from '@/store'

const calculated = computed(() => {
  return store.matchResult
})

async function calculate() {
  if (store.targetImage) {
    await uploadFile()
  }
}
</script>

<template>
  <button class="compare-button" v-if="!calculated" @click="calculate">
    compare faces
  </button>
  <button class="result" v-else>
    <img
      src="@/components/icons/info.svg"
      alt="Info"
      @click="store.toggleInfo"
    />
    <div>%{{ store.matchResult?.[store.selectedResultIndex]?.similarity }}</div>
    <img
      src="@/components/icons/refresh.svg"
      alt="Refresh"
      @click="store.reset"
    />
  </button>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400..900&display=swap');

.compare-button {
  border: 5px solid #fee1e0;
  height: 10vh;
  width: 300px;
  border-radius: 50px;
  color: #92120c;
  font-weight: bold;
  text-transform: uppercase;
  font-size: 20px;
  cursor: pointer;
}
.result {
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  border: 5px solid #fee1e0;
  height: 10vh;
  width: 300px;
  border-radius: 50px;
  color: #92120c;
  font-weight: bold;
  font-size: 30px;
  font-family: 'Orbitron', serif;
  font-optical-sizing: auto;
  font-weight: bold;
  font-style: normal;
}

.result img {
  height: 30px;
  cursor: pointer;
}
</style>

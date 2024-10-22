<script setup lang="ts">
import { store } from '@/store'
import { ref, watchEffect } from 'vue'

const info = ref('')

const fetchInfo = async () => {
  try {
    const url = `http://localhost:5000/faces/${store.matchResult?.[store.selectedResultIndex].info}`
    const response = await fetch(url)
    if (response.ok) {
      const data = await response.text()
      info.value = data
    } else {
      info.value = 'Erro ao buscar informações'
    }
  } catch (error) {
    store.showInfo = false
    store.error = error as string
  }
}

watchEffect(() => {
  if (store.matchResult && store.selectedResultIndex !== undefined) {
    fetchInfo()
  }
})
</script>

<template>
  <div class="info-container">
    <div class="exit-icon" @click="store.toggleInfo">
      <img src="@/components/icons/close.svg" alt="Close" />
    </div>
    <div class="title">Informações</div>
    <div class="info">
      {{ info }}
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap');

.info-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 30px;
  font-family: 'Inter', sans-serif;
  font-optical-sizing: auto;
  font-style: normal;
  width: 300px;
  padding: 10px;
  height: 100%;
}

.title {
  color: #4b4b4b;
  font-weight: 600;
  font-size: 20px;
}

.exit-icon {
  margin-left: auto;
}

.info {
  border: 1px solid #d0d5dd;
  border-radius: 5px;
  padding: 2%;
  height: 30vh;
  width: 100%;
  overflow-y: auto;
  white-space: pre-wrap;
}
</style>

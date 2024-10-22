<script setup lang="ts">
import { store } from '@/store'
</script>

<template>
  <div class="error-container">
    <div class="exit-icon" @click="store.clearError">
      <img src="@/components/icons/close.svg" alt="Close" />
    </div>
    <div class="title">Erro!</div>
    <div class="error">
      {{ store.error }}
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap');

.error-container {
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

.error {
  border: 1px solid #d0d5dd;
  border-radius: 5px;
  padding: 2%;
  height: 30vh;
  width: 100%;
}
</style>

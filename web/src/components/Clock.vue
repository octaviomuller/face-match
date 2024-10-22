<script setup lang="ts">
import { store } from '@/store'
import { computed, onBeforeMount, onBeforeUnmount, ref } from 'vue'

const currentTime = ref(null as string | null)

const updateCurrentTime = () => {
  const now = new Date()
  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  const timeFormatted = `${hours}:${minutes}`

  currentTime.value = timeFormatted
}

const updateTimeInterval = setInterval(updateCurrentTime, 1000)

onBeforeMount(() => {
  updateCurrentTime()
})

onBeforeUnmount(() => {
  clearInterval(updateTimeInterval)
})
</script>

<template>
  <div class="overlay-button-result" @click="store.toggleResult">
    {{ currentTime }}
  </div>
</template>

<style scoped>
.overlay-button-result {
  position: absolute;
  top: 0;
  left: 0;
  margin: 5px;
  font-size: 18px;
  font-weight: 400;
  cursor: pointer;
}
</style>

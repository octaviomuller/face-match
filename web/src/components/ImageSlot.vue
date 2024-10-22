<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { store } from '@/store'
import userIcon from '@/components/icons/user.svg'

const props = defineProps({
  disable: Boolean,
  position: String,
})

const selectedImage = ref<string | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)

const handleImageChange = (event: Event) => {
  const target = event.target as HTMLInputElement

  if (target.files && target.files.length > 0) {
    const file = target.files[0]
    const reader = new FileReader()

    reader.onload = e => {
      selectedImage.value = e.target?.result as string
      store.targetImage = file
    }

    reader.readAsDataURL(file)
  }
}

watch(
  () => store.targetImage,
  newVal => {
    if (newVal === null) {
      selectedImage.value = null
    }
  },
)

const tapToAddText = computed(() => {
  return !(selectedImage.value || (props.disable && store.matchResult?.length))
})

const imgSrc = computed(() => {
  if (props.disable && store.matchResult?.length)
    return `http://localhost:5000/faces/${store.matchResult?.[store.selectedResultIndex].name}`

  return selectedImage.value || userIcon
})
</script>

<template>
  <div class="image-slot" @click="fileInput?.click()">
    <input
      v-if="!disable"
      type="file"
      ref="fileInput"
      accept="image/*"
      @change="handleImageChange"
      style="display: none"
    />
    <img :src="imgSrc" alt="User SVG" />
    <div class="text-overlay" v-if="tapToAddText">
      Tap to add {{ position }} image
    </div>
  </div>
</template>

<style scoped>
.image-slot {
  height: 30vh;
  width: 30vh;
  border-radius: 50%;
  background-color: white;
  border: 5px solid white;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  position: relative;
  cursor: pointer;
}

img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.text-overlay {
  position: absolute;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: black;
  text-align: center;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1;
}
</style>

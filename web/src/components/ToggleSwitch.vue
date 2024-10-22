<script setup lang="ts">
import { ref, watch } from 'vue'
import { store } from '@/store'

const props = defineProps<{
  name: 'Sexo' | 'Categoria'
  firstOption: string
  secondOption: string
}>()

const id = 'toggle-' + props.name

const isChecked = ref(
  props.name === 'Sexo'
    ? store.filters.gender === props.secondOption
    : store.filters.category === props.secondOption,
)

watch(isChecked, newVal => {
  if (props.name === 'Sexo') {
    store.filters.gender = newVal ? 'Mulheres' : 'Homens'
  } else {
    store.filters.category = newVal ? 'Moto' : 'Carro'
  }
})
</script>

<template>
  <input type="checkbox" :id="id" class="toggleCheckbox" v-model="isChecked" />
  <label :for="id" class="toggleContainer">
    <div>{{ firstOption }}</div>
    <div>{{ secondOption }}</div>
  </label>
</template>

<style scoped>
.toggleContainer {
  position: relative;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  border-radius: 20px;
  background: #f2f4f7;
  font-weight: bold;
  cursor: pointer;
  width: 100%;
}
.toggleContainer::before {
  content: '';
  position: absolute;
  width: 50%;
  height: 100%;
  left: 0%;
  border-radius: 20px;
  background: #2b67f6;
  transition: all 0.3s;
}
.toggleContainer div {
  padding: 10px;
  text-align: center;
  z-index: 1;
}
.toggleCheckbox:checked + .toggleContainer::before {
  left: 50%;
}
.toggleCheckbox {
  display: none;
}
.toggleCheckbox:checked + .toggleContainer div:first-child {
  color: #98a0b4;
  transition: color 0.3s;
}
.toggleCheckbox:checked + .toggleContainer div:last-child {
  color: white;
  transition: color 0.3s;
}
.toggleCheckbox + .toggleContainer div:first-child {
  color: white;
  transition: color 0.3s;
}
.toggleCheckbox + .toggleContainer div:last-child {
  color: #98a0b4;
  transition: color 0.3s;
}
</style>

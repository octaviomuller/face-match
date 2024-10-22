<script setup lang="ts">
import { store } from '@/store'
import ToggleSwitch from '@/components/ToggleSwitch.vue'

const updateName = (event: Event) => {
  store.filters.name = (event.target as HTMLInputElement).value
}

const updateCheckbox1 = (event: Event) => {
  store.filters.checkbox1 = (event.target as HTMLInputElement).checked
}

const updateCheckbox2 = (event: Event) => {
  store.filters.checkbox2 = (event.target as HTMLInputElement).checked
}
</script>

<template>
  <div class="filter-container">
    <div class="exit-icon" @click="store.toggleFilters">
      <img src="@/components/icons/close.svg" alt="Close" />
    </div>
    <div class="title">Filtros</div>

    <label>Nome</label>

    <input
      class="input-name"
      placeholder="Lucas Almeida, Henrique, Carlos Viana Texeira"
      :value="store.filters.name"
      @input="updateName"
    />

    <label>Sexo</label>

    <ToggleSwitch
      name="Sexo"
      first-option="Homens ♂"
      second-option="Mulheres ♀"
    ></ToggleSwitch>

    <label>Categoria</label>

    <ToggleSwitch
      name="Categoria"
      first-option="Carro"
      second-option="Moto"
    ></ToggleSwitch>

    <label>Pastas</label>

    <div class="checkbox-container">
      <input
        type="checkbox"
        :checked="store.filters.checkbox1"
        @change="updateCheckbox1"
      />
      <div>Usados 1</div>
    </div>

    <div class="checkbox-container">
      <input
        type="checkbox"
        :checked="store.filters.checkbox2"
        @change="updateCheckbox2"
      />
      <div>Usados 2</div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap');

.filter-container {
  display: flex;
  flex-direction: column;
  align-items: start;
  gap: 30px;
  font-family: 'Inter', sans-serif;
  font-optical-sizing: auto;
  font-style: normal;
  width: 300px;
  height: 100%;
  padding: 10px;
}

.title {
  color: #4b4b4b;
  font-weight: 600;
  font-size: 20px;
}

.input-name {
  border-radius: 8px;
  border: 2px solid #d0d5dd;
  width: 100%;
  height: fit-content;
  padding: 10px;
  box-sizing: border-box;
}

.checkbox-container {
  display: flex;
  flex-direction: row;
  gap: 3px;
}

label {
  color: #98a0b4;
  font-family: 'Inter', sans-serif;
  font-optical-sizing: auto;
  font-style: normal;
  font-weight: 600;
}

.exit-icon {
  margin-left: auto;
  cursor: pointer;
}
</style>

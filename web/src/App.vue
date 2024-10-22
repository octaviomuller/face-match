<script setup lang="ts">
import ImageSlot from './components/ImageSlot.vue'
import Clock from '@/components/Clock.vue'
import Error from '@/components/Error.vue'
import Info from '@/components/Info.vue'
import CompareButton from './components/CompareButton.vue'
import Overlay from '@/components/Overlay.vue'
import Result from '@/components/Result.vue'
import Filters from '@/components/Filters.vue'
import { store } from '@/store'
</script>

<template>
  <main>
    <ImageSlot position="first"></ImageSlot>
    <CompareButton></CompareButton>
    <ImageSlot position="second" :disable="true"></ImageSlot>
    <Overlay
      v-if="
        !store.error &&
        (store.showFilters || store.showResult || store.showInfo)
      "
    >
      <Filters v-if="store.showFilters"></Filters>
      <Result v-if="store.showResult"></Result>
      <Info v-if="store.showInfo"></Info>
    </Overlay>
    <Overlay v-if="store.error">
      <Error></Error>
    </Overlay>
    <Clock></Clock>
    <img
      src="@/components/icons/battery.svg"
      class="overlay-button-filters"
      @click="store.toggleFilters"
    />
    <div class="hidden-selector-left" @click="store.previousMatch"></div>
    <div class="hidden-selector-right" @click="store.nextMatch"></div>
  </main>
</template>

<style scoped>
main {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  align-items: center;
  min-height: 100vh;
}
.overlay-button-filters {
  position: absolute;
  top: 0;
  right: 0;
  margin: 5px;
  height: 20px;
  cursor: pointer;
}

.hidden-selector-left {
  position: absolute;
  height: 95vh;
  left: 0;
  bottom: 0;
  width: 5vw;
  pointer-events: all;
}
.hidden-selector-right {
  position: absolute;
  height: 95vh;
  right: 0;
  bottom: 0;
  width: 5vw;
  pointer-events: all;
}
</style>

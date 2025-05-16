<script setup>
import UserInput from './components/UserInput.vue'
</script>

<template>
  <UserInput class="user-input"/>
</template>

<style scoped>
.input-wrapper {
  border: 2px solid #ccc;
  padding: 1rem;
  border-radius: 0.5rem;
  width: fit-content;
  margin: 2rem auto;
  display: block; /* make sure it behaves like a block element */
}
</style>

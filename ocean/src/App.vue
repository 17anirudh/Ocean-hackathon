<script setup>
import UserInput from './components/UserInput.vue'
import Output from './components/Output.vue'
import { ref } from 'vue'

const data = ref(null)

function handleData(newData) {
  data.value = newData
}
</script>

<template>
  <div class="first">
    <header>
      <p>Veteran Hunting</p>
    </header>
  </div>
  <div class="UserInput">
    <UserInput @dataReady="handleData" />
  </div>
  <div class="Output">
    <Output :data="data" />
  </div>
</template>

<style>
*{
  margin: 0;
  padding: 0;
}
body{
  display: flex;
  flex-direction: column;
  width: 100%;
}
header {
  display: fixed;
  top: 0;
  margin-top: 0;
  width: 100%;
  font-size: clamp(0.75rem, -0.3415rem + 5.893vw, 2.9rem);
  text-align: center;
  margin-bottom: 10vh;
}
.UserInput {
  border: 2px solid wheat;
  width: 50%;
  justify-content: center;
  align-items: center;
  margin-left: 15vw;
  margin-bottom: 7vh;
  display: flex;
}
.Output {
  width: 90%;
  margin-left: 3vw;
  justify-content: center;
  align-items: center;
  display: flex;
}
</style>

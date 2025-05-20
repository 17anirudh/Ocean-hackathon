<script setup>
import UserInput from './components/UserInput.vue'
import Output from './components/Output.vue'
import { ref } from 'vue'

const data = ref(null)

function handleData(newData) {
  data.value = newData
  console.log('Data received from UserInput:', newData)
}
</script>

<template>
  <header>
    Veteran Hunting
  </header>
  <div class="UserInput">
    <UserInput @dataReady="handleData" />
  </div>
  <div class="output">
    <Output :data="data" />
  </div>
</template>

<style>
*{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
body{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
}
header {
  font-size: clamp(0.75rem, -0.3815rem + 4.893vw, 2.75rem);
  text-align: center;
  }
.UserInput {
  margin-top: 5vw;
  width: fit-content;
  border: 2px black solid;
  border-radius: 23px;
  }
</style>

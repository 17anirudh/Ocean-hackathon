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
@import url('https://fonts.googleapis.com/css2?family=Edu+AU+VIC+WA+NT+Pre:wght@400..700&family=Playpen+Sans+Hebrew:wght@100..800&family=Roboto+Flex:opsz,wdth,wght@8..144,125,100..1000&display=swap');
*{
  margin: 0;
  padding: 0;
}
body{
  display: flex;
  flex-direction: column;
  width: 100%;
  font-family: 'Playpen Sans Hebrew', cursive;
}
header {
  color: aliceblue;
  display: fixed;
  top: 0;
  margin-top: 0;
  width: 100%;
  font-size: clamp(0.75rem, -0.3415rem + 5.893vw, 2.9rem);
  text-align: center;
  margin-bottom: 10vh;
  font-family: 'Playpen Sans Hebrew', cursive;
}
.UserInput {
  min-width: 99vw;
  max-width: 99vw;
  justify-content: center;
  align-items: center;
  display: flex;
  font-family: 'Playpen Sans Hebrew', cursive;
  font-size: clamp(0.75rem, 0.1843rem + 2.4465vw, 1.75rem);
}
.Output {
  width: 90%;
  margin-left: 3vw;
  justify-content: center;
  padding-top: -10vh;
  align-items: center;
  display: flex;
  font-family: 'Playpen Sans Hebrew', cursive;
  font-size: clamp(0.75rem, 0.1843rem + 2.4465vw, 1.75rem);
}
</style>

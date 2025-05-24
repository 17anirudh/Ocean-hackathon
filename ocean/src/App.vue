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
  <div class="footer">
    <footer>
      <span class="text">Made using </span>
      <span class="gemini">
        <a href="https://gemini.google.com/app" target="_blank" rel="noopener noreferrer">
          <img src="https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d4735304ff6292a690345.svg" alt="Gemini Logo" width="40" height="40">
        </a>
      </span>
      <span class="google">
        <a href="https://www.google.com/" target="_blank" rel="noopener noreferrer">
          <img src="https://www.google.com/favicon.ico" alt="Google Logo" width="40" height="40">
        </a>
      </span>
      <span class="vue">
        <a href="https://vuejs.org/" target="_blank" rel="noopener noreferrer">
          <img src="/src/assets/favicon.ico" alt="Vue Logo" width="40" height="40">
        </a>
      </span>
      <span class="flask">
        <a href="https://flask.palletsprojects.com/" target="_blank" rel="noopener noreferrer">
          <img src="https://upload.wikimedia.org/wikipedia/commons/3/3c/Flask_logo.svg" alt="Flask Logo" width="70" height="40">
        </a>
      </span>
      <span class="bun">
        <a href="https://bun.sh/" target="_blank" rel="noopener noreferrer">
          <img src="https://bun.sh/logo.svg" alt="Bun Logo" width="40" height="40">
        </a>
      </span>
    </footer>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Edu+AU+VIC+WA+NT+Pre:wght@400..700&family=Playpen+Sans+Hebrew:wght@100..800&family=Roboto+Flex:opsz,wdth,wght@8..144,125,100..1000&display=swap');
*{
  margin: 0;
  padding: 0;
}
body{
  height: 100%;
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
footer {
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
}
span.flask > a{
  color: aliceblue;
}
</style>

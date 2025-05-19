<script setup>
import UserInput from './components/UserInput.vue'
</script>

<template>
  <header>
    Veteran Hunting
  </header>
  <div class="UserInput">
    <UserInput />
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
  width: 100%;
}
header {
  font-size: clamp(0.75rem, -0.3815rem + 4.893vw, 2.75rem);
  text-align: center;
  }
.UserInput {
  margin-top: 7vw;
  margin-right: 20vw;
  margin-left: 20vw;
  width: fit-content;
  border: 2px black solid;
  border-radius: 23px;
  }
</style>

<template>
  <table v-if="data && data.length" cellpadding="10">
    <thead>
      <tr>
        <th>#</th>
        <th>Domain</th>
        <th>Subdomain</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(item, index) in data" :key="index">
        <td>{{ index + 1 }}</td>
        <td>{{ item.domain }}</td>
        <td>{{ item.subdomain }}</td>
      </tr>
    </tbody>
  </table>

  <p v-else>No data received 🫠</p>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
    data: {
        type: Array,
        required: true
    }
})
</script>
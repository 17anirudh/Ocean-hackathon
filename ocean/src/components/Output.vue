<template>
  <div>
    <table v-if="Array.isArray(data) && data.length" cellpadding="10">
      <thead>
        <tr>
          <th>#</th>
          <th>Name</th>
          <th>Work/Location</th>
          <th>LinkedIn</th>
          <th>Bio</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in data" :key="index">
          <td>{{ index + 1 }}</td>
          <td>{{ item.name }}</td>
          <td>{{ item.work_or_location }}</td>
          <td>
            <a :href="item.contact" target="_blank">{{ item.contact }}</a>
          </td>
          <td>{{ item.about }}</td>
        </tr>
      </tbody>
    </table>

    <div v-else-if="typeof data === 'string'">
      No data found.
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  data: {
    type: [String, Object, null],
    default: null
  }
})
  
if (typeof props.data === 'string') {
  props.data = props.data.trim()
  props.data = props.data.replace(/\\n/g, '\n')
  props.data = JSON.parse(props.data)
} else if (typeof props.data === 'object') {
  props.data = JSON.stringify(props.data, null, 2)
} else {
  props.data = null
}
</script>

<style scoped>
table {
  width: 95%;
  margin: 10vw auto;
  border-collapse: collapse;
  border: 2px solid red;
}
tr, td{
  border: 2px solid red;
  padding: 10px;
  text-align: center;
}
</style>

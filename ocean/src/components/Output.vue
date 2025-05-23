<template>
  <div>
    <table v-if="Array.isArray(data) && data.length" cellpadding="10">
      <thead>
        <tr>
          <th>#</th>
          <th>Name</th>
          <th>Work/Location</th>
          <th>LinkedIn</th>
          <th>Confidence Score</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in data" :key="index">
          <td>{{ index + 1 }}</td>
          <td>{{ item.name }}</td>
          <td>{{ item.work_or_location }}</td>
          <td>
            <a :href="item.contact" target="_blank">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-linkedin" viewBox="0 0 16 16">
                <path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854zm4.943 12.248V6.169H2.542v7.225zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248S2.4 3.226 2.4 3.934c0 .694.521 1.248 1.327 1.248zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016l.016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225z"/>
              </svg>
            </a>
          </td>
          <td>{{ item.confidence_score }}</td>
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
tr, td, th{
  border: 2px solid purple;
  padding: 10px;
  text-align: center;
}
</style>

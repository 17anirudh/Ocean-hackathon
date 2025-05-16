<template>
  <div class="typeaface-container">
    <!-- Domain Typeahead -->
    <div class="domain-box">
        <input v-model="domainInput" @input="filterDomains" @keydown.down.prevent="moveDown('domain')" @keydown.up.prevent="moveUp('domain')" 
        @keydown.enter.prevent="selectDomain" placeholder="Domain..." title="Domain"/>
        <ul v-if="filteredDomains.length">
        <li v-for="(domain, index) in filteredDomains" :key="domain" :class="{ selected: index === selectedDomainIndex }" @click="selectDomain(index)">
            {{ domain }}
        </li>
        </ul>
  </div>
  <!-- Subdomain Typeahead -->
    <div class="subdomain-box">
      <input v-model="subdomainInput" @input="filterSubdomains" @keydown.down.prevent="moveDown('subdomain')" @keydown.up.prevent="moveUp('subdomain')"
        @keydown.enter.prevent="selectSubdomain" placeholder="Subdomain..." title="Keywords"/>
      <ul v-if="filteredSubdomains.length">
        <li v-for="(sub, index) in filteredSubdomains" :key="sub" :class="{ selected: index === selectedSubdomainIndex }" @click="selectSubdomain(index)">
          {{ sub }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const data = ref({})
const domains = ref([])
const filteredDomains = ref([])
const selectedDomain = ref('')
const domainInput = ref('')
const selectedDomainIndex = ref(0)

const subdomains = ref([])
const filteredSubdomains = ref([])
const subdomainInput = ref('')
const selectedSubdomainIndex = ref(0)

// Fetch data
onMounted(async () => {
  const res = await fetch('/output.json')
  const json = await res.json()
  data.value = json
  domains.value = Object.keys(json)
})

// Filter domains
function filterDomains() {
  filteredDomains.value = domains.value.filter((d) =>
    d.toLowerCase().includes(domainInput.value.toLowerCase())
  ).slice(0, 5)
  selectedDomainIndex.value = 0
}

// Select domain
function selectDomain(index = selectedDomainIndex.value) {
  selectedDomain.value = filteredDomains.value[index]
  subdomains.value = data.value[selectedDomain.value]
  domainInput.value = selectedDomain.value
  filteredDomains.value = []
  subdomainInput.value = ''
  filteredSubdomains.value = []
}

// Filter subdomains
function filterSubdomains() {
  filteredSubdomains.value = subdomains.value.filter((s) =>
    s.toLowerCase().includes(subdomainInput.value.toLowerCase())
  ).slice(0, 5)
  selectedSubdomainIndex.value = 0
}

// Select subdomain
function selectSubdomain(index = selectedSubdomainIndex.value) {
  subdomainInput.value = filteredSubdomains.value[index]
  filteredSubdomains.value = []
}

// Keyboard nav helpers
function moveDown(type) {
  if (type === 'domain') {
    if (selectedDomainIndex.value < filteredDomains.value.length - 1)
      selectedDomainIndex.value++
  } else {
    if (selectedSubdomainIndex.value < filteredSubdomains.value.length - 1)
      selectedSubdomainIndex.value++
  }
}

function moveUp(type) {
  if (type === 'domain') {
    if (selectedDomainIndex.value > 0) selectedDomainIndex.value--
  } else {
    if (selectedSubdomainIndex.value > 0) selectedSubdomainIndex.value--
  }
}
</script>

<style scoped>
.typeaface-container {
  display: flex;
  gap: 1rem;
}

.domain-box,
.subdomain-box {
  flex: 1;
}

.selected {
  outline: 1px dashed black;
}
ul {
  margin: 0;
  padding: 0;
  list-style: none;
}
li {
  cursor: pointer;
}
</style>

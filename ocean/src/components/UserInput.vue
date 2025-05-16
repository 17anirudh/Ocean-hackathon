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
   <!-- Submit Button -->
  <div class="submit-box">
      <button @click="submitSelection">Submit</button>
  </div>
  <!-- Display result -->
  <p v-if="resultText" class="result-text">{{ resultText }}</p>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Fuse from 'fuse.js'

const data = ref({})
const flatData = ref([])

const domainInput = ref('')
const filteredDomains = ref([])
const selectedDomainIndex = ref(0)
const selectedDomain = ref('')

const subdomainInput = ref('')
const filteredSubdomains = ref([])
const selectedSubdomainIndex = ref(0)
const resultText = ref('')


let fuseDomains = null
let fuseSubdomains = null

function submitSelection() {
  if (!selectedDomain.value && !subdomainInput.value) {
    resultText.value = 'Please select domain and/or subdomain.'
    return
  }
  resultText.value = `You selected Domain: "${selectedDomain.value || 'None'}" and Subdomain: "${subdomainInput.value || 'None'}"`
}

onMounted(async () => {
  const res = await fetch('/output.json')
  const json = await res.json()
  data.value = json

  // flatten your data: [{domain, subdomain}, ...]
  flatData.value = []
  for (const domain in json) {
    json[domain].forEach(sub => {
      flatData.value.push({ domain, subdomain: sub })
    })
  }

  // fuse for domains (search only domain key)
  fuseDomains = new Fuse(flatData.value, {
    keys: ['domain'],
    threshold: 0.3,
  })

  // fuse for subdomains (search only subdomain key)
  fuseSubdomains = new Fuse(flatData.value, {
    keys: ['subdomain'],
    threshold: 0.3,
  })
})

function filterDomains() {
  if (!domainInput.value) {
    filteredDomains.value = []
    return
  }
  // get unique domain results from fuse search
  const results = fuseDomains.search(domainInput.value).slice(0, 10)
  const uniqueDomains = [...new Set(results.map(r => r.item.domain))]
  filteredDomains.value = uniqueDomains.slice(0, 5)
  selectedDomainIndex.value = 0
}

function selectDomain(index = selectedDomainIndex.value) {
  selectedDomain.value = filteredDomains.value[index]
  domainInput.value = selectedDomain.value
  filteredDomains.value = []
  subdomainInput.value = ''
  filteredSubdomains.value = []
}

function filterSubdomains() {
  if (!subdomainInput.value || !selectedDomain.value) {
    filteredSubdomains.value = []
    return
  }
  // search subdomains, but filter to only those with selected domain
  const results = fuseSubdomains.search(subdomainInput.value)
  const filteredByDomain = results.filter(r => r.item.domain === selectedDomain.value)
  filteredSubdomains.value = filteredByDomain.slice(0, 5).map(r => r.item.subdomain)
  selectedSubdomainIndex.value = 0
}

function selectSubdomain(index = selectedSubdomainIndex.value) {
  subdomainInput.value = filteredSubdomains.value[index]
  filteredSubdomains.value = []
}

// keyboard navigation helpers like before
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
  background-color: aliceblue;
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
  color: black;
}
li {
  cursor: pointer;
  color: black;
}
.submit-box {
  display: flex;
  align-items: center;
}

.submit-box button {
  padding: 0.5rem 1rem;
  cursor: pointer;
}

.result-text {
  margin-top: 1rem;
  font-weight: 600;
  color: #333;
}
</style>

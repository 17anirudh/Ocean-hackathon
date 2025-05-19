<template>
  <div class="MAIN_DIV">
    <div class="typeaface-container">
      <!-- Domain Typeahead -->
      <div class="domain-box">
        <input v-model="domainInput" @input="filterDomains" @keydown.down.prevent="moveDown('domain')" @keydown.up.prevent="moveUp('domain')" 
          @keydown.enter.prevent="selectDomain" class="domainInput" placeholder="domain..." title="Domain"/>
        <ul v-if="filteredDomains.length">
          <li v-for="(domain, index) in filteredDomains" :key="domain" :class="{ selected: index === selectedDomainIndex }" @click="selectDomain(index)">
              {{ domain }}
          </li>
        </ul>
      </div>
      <!-- Subdomain Typeahead -->
      <div class="subdomain-box">
        <input v-model="subdomainInput" @input="filterSubdomains" @keydown.down.prevent="moveDown('subdomain')" @keydown.up.prevent="moveUp('subdomain')"
          @keydown.enter.prevent="selectSubdomain" class="subdomainInput" placeholder="keywords..." title="Keywords"/>
        <ul v-if="filteredSubdomains.length">
          <li v-for="(sub, index) in filteredSubdomains" :key="sub" :class="{ selected: index === selectedSubdomainIndex }" @click="selectSubdomain(index)">
            {{ sub }}
          </li>
        </ul>
      </div>
    </div>
    <!-- Submit Button -->
    <div class="submit-box">
      <button @click="submitSelection" class="submit-button">Submit</button>
    </div>
    <!-- Display result -->
    <div class="result-box">
      <p v-if="resultText" class="result-text">{{ resultText }}</p>
    </div>
  </div>
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
.MAIN_DIV {
  display: flex;
  flex-direction: column;
  padding: 3vw;
  border: 2px solid #000;
  border-radius: 10px;
  font-size: clamp(0.75rem, -0.3815rem + 4.893vw, 2.75rem);
  background: linear-gradient(45deg, #000, #252323);
  height: fit-content;
}
.typeaface-container {
  display: flex;
  flex-direction: row;
  margin-bottom: 5vw;
  font-size: clamp(0.75rem, 0.4954rem + 1.1009vw, 1.2rem);
  justify-content: space-evenly;
}

.domainInput, .subdomainInput {
  color: white;
  border: 2px solid #8707ff;
  border-radius: 10px;
  padding: 10px 25px;
  background: transparent;
  font-size: clamp(0.75rem, 0.1843rem + 2.4465vw, 1.rem);
  max-width: 190px;
}

.domainInput:active {
  box-shadow: 2px 2px 15px #8707ff inset;
}
.subdomainInput:active{
  box-shadow: 2px 2px 15px #8707ff inset;
}

ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
  border: 2px solid #8707ff;
  border-radius: 10px;
  max-width: 190px;
  background: black;
  color: white;
  overflow: hidden;
  box-shadow: 0 0 10px #8707ff55;
  position: absolute;
  z-index: 10;
}

li {
  padding: 10px 25px;
  cursor: pointer;
  transition: all 0.2s ease;
}

li:hover,
li.selected {
  background-color: #8707ff55;
  color: #fff;
}


.submit-box {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 5vw;
}

.submit-button {
  cursor: pointer;
  font-size: large;
  font-family: inherit;
  font-weight: bold;
  color: #0011ff;
  background-color: black;
  padding: 0.8em 2.2em;
  border-radius: 50em;
  border: 6px solid #8b93f8;
  box-shadow: 0px 8px #1f35ff;
  transition: all 0.3s ease;
}
.submit-button:active {
  position: relative;
  top: 8px;
  border: 6px solid #646fff;
  box-shadow: 0px 0px;
}
.submit-button:hover {
  background-color: #0011ff;
  color: white;
  box-shadow: 0px 8px #646fff;
}

.result-box {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 5vw;
  font-size: clamp(0.75rem, 0.6439rem + 0.4587vw, 0.9375rem);
}

</style>

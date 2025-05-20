<template>
  <div class="MAIN_DIV">
    <div class="typeaface-container">
      <!-- Domain Typeahead -->
      <div class="domain-box">
        <input 
          v-model="domainInput" 
          @input="filterDomains" 
          @keydown.down.prevent="moveDown('domain')" 
          @keydown.up.prevent="moveUp('domain')" 
          @keydown.enter.prevent="selectDomain" 
          class="domainInput" 
          placeholder="domain..." 
          title="Domain"
        />
        <ul v-if="filteredDomains.length">
          <li v-for="(domain, index) in filteredDomains" :key="domain" :class="{ selected: index === selectedDomainIndex }" @click="selectDomain(index)">
              {{ domain }}
          </li>
        </ul>
      </div>
      <!-- Subdomain Typeahead -->
      <div class="subdomain-box">
        <input 
          v-model="subdomainInput" 
          @input="filterSubdomains" 
          @keydown.down.prevent="moveDown('subdomain')" 
          @keydown.up.prevent="moveUp('subdomain')"
          @keydown.enter.prevent="selectSubdomain" 
          class="subdomainInput" 
          placeholder="keywords..." 
          title="Keywords"
        />
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

const emit = defineEmits(['dataReady'])

const data = ref({})
const flatData = ref([])

const domainInput = ref('')
const subdomainInput = ref('')
const selectedDomain = ref('')

const filteredDomains = ref([])
const filteredSubdomains = ref([])

const selectedDomainIndex = ref(0)
const selectedSubdomainIndex = ref(0)

const resultText = ref('')

let fuseDomains = null
let fuseSubdomains = null

onMounted(async () => {
  const res = await fetch('/output.json')
  const json = await res.json()
  data.value = json

  flatData.value = Object.entries(json).flatMap(([domain, subs]) =>
    subs.map(sub => ({ domain, subdomain: sub }))
  )

  fuseDomains = new Fuse(flatData.value, {
    keys: ['domain'],
    threshold: 0.3,
  })

  fuseSubdomains = new Fuse(flatData.value, {
    keys: ['subdomain'],
    threshold: 0.3,
  })
})

function filterDomains() {
  if (!domainInput.value) return (filteredDomains.value = [])

  const results = fuseDomains.search(domainInput.value).map(r => r.item.domain)
  filteredDomains.value = [...new Set(results)].slice(0, 5)
  selectedDomainIndex.value = 0
}

function filterSubdomains() {
  if (!subdomainInput.value || !selectedDomain.value)
    return (filteredSubdomains.value = [])

  const results = fuseSubdomains.search(subdomainInput.value)
  const matches = results.filter(r => r.item.domain === selectedDomain.value)
  filteredSubdomains.value = matches.map(r => r.item.subdomain).slice(0, 5)
  selectedSubdomainIndex.value = 0
}

function selectDomain(index = selectedDomainIndex.value) {
  selectedDomain.value = filteredDomains.value[index]
  domainInput.value = selectedDomain.value
  filteredDomains.value = []
  subdomainInput.value = ''
  filteredSubdomains.value = []
}

function selectSubdomain(index = selectedSubdomainIndex.value) {
  subdomainInput.value = filteredSubdomains.value[index]
  filteredSubdomains.value = []
}

function moveDown(type) {
  const list = type === 'domain' ? filteredDomains.value : filteredSubdomains.value
  const indexRef = type === 'domain' ? selectedDomainIndex : selectedSubdomainIndex

  if (indexRef.value < list.length - 1) indexRef.value++
}

function moveUp(type) {
  const indexRef = type === 'domain' ? selectedDomainIndex : selectedSubdomainIndex

  if (indexRef.value > 0) indexRef.value--
}

// untouched by request
async function submitSelection() {
  const domain = domainInput.value.trim()
  const subdomain = subdomainInput.value.trim()

  if (!domain && !subdomain) {
    resultText.value = 'Please select domain and/or subdomain.'
    return
  }

  try {
    const res = await fetch('http://127.0.0.1:5000/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ domain, subdomain }),
    })
    const data = await res.json()
    emit('dataReady', data)
  } catch (err) {
    emit('dataReady', { error: err.message })
  }
}

</script>


<style scoped>
.MAIN_DIV {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  height: fit-content;
  padding: 20px;
}
.typeaface-container {
  display: flex;
  flex-direction: row;
  font-size: clamp(0.75rem, 0.4954rem + 1.1009vw, 1.2rem);
  gap: 1vw;
}

.domainInput, .subdomainInput {
  color: white;
  border: 2px solid #8707ff;
  border-radius: 10px;
  padding: 10px 25px;
  background: transparent;
  font-size: clamp(0.75rem, 0.1843rem + 2.4465vw, 1.rem);
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
  color: #fff;
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

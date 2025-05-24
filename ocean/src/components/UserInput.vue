<template>
  <div class="MAIN_DIV">
    <div class="typeaface-container">
      <!-- Domain Typeahead -->
      <div class="domain-box">
        <input 
          v-model="domainInput" 
          @input="filterDomains" 
          @focus="showDomainDropdown = true"
          @blur="handleDomainBlur"
          @keydown.down.prevent="moveDown('domain')" 
          @keydown.up.prevent="moveUp('domain')" 
          @keydown.enter.prevent="selectDomain" 
          class="domainInput" 
          placeholder="domain..." 
          title="Domain"
        />
        <div class="dropdown-wrapper">
          <ul v-if="filteredDomains.length && showDomainDropdown" class="dropdown-list">
            <li v-for="(domain, index) in filteredDomains" 
                :key="domain" 
                :class="{ selected: index === selectedDomainIndex }" 
                @click="selectDomain(index)"
                @mousedown.prevent>
              {{ domain }}
            </li>
          </ul>
        </div>
      </div>
      <!-- Subdomain Typeahead -->
      <div class="subdomain-box">
        <input 
          v-model="subdomainInput" 
          @input="filterSubdomains" 
          @focus="showSubdomainDropdown = true"
          @blur="handleSubdomainBlur"
          @keydown.down.prevent="moveDown('subdomain')" 
          @keydown.up.prevent="moveUp('subdomain')"
          @keydown.enter.prevent="selectSubdomain" 
          class="subdomainInput" 
          placeholder="keywords..." 
          title="Keywords"
        />
        <div class="dropdown-wrapper">
          <ul v-if="filteredSubdomains.length && showSubdomainDropdown" class="dropdown-list">
            <li v-for="(sub, index) in filteredSubdomains" 
                :key="sub" 
                :class="{ selected: index === selectedSubdomainIndex }" 
                @click="selectSubdomain(index)"
                @mousedown.prevent>
              {{ sub }}
            </li>
          </ul>
        </div>
      </div>
    </div>
    <!-- Submit Button -->
    <div class="submit-box">
      <button @click="submitSelection" class="submit-button" :disabled="isLoading" title="Submit">Submit</button>
    </div>
    <!-- Display result -->
    <div class="result-box">
      <span v-if="isLoading" class="loader"></span>
      <p v-else-if="resultText" class="result-text">{{ resultText }}</p>
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
const showDomainDropdown = ref(false)
const showSubdomainDropdown = ref(false)
let fuseDomains = null
let fuseSubdomains = null
const isLoading = ref(false)

onMounted(async () => {
  try {
    const res = await fetch('/output.json')
    const json = await res.json()
    data.value = json

    flatData.value = Object.entries(json).flatMap(([domain, subs]) =>
      subs.map(sub => ({ domain, subdomain: sub }))
    )

    fuseDomains = new Fuse(flatData.value, {
      keys: ['domain'],
      threshold: 0.4, // Slightly more lenient threshold
    })

    fuseSubdomains = new Fuse(flatData.value, {
      keys: ['subdomain'],
      threshold: 0.4, // Slightly more lenient threshold
    })

    // Initial filtering
    if (domainInput.value) filterDomains()
    if (subdomainInput.value) filterSubdomains()
  } catch (error) {
    console.error("Error loading data:", error)
    resultText.value = "Error loading data. Please try again."
  }
})

function filterDomains() {
  if (!domainInput.value) {
    filteredDomains.value = []
    return
  }

  if (!fuseDomains) return // Safety check

  const results = fuseDomains.search(domainInput.value).map(r => r.item.domain)
  filteredDomains.value = [...new Set(results)].slice(0, 5)
  selectedDomainIndex.value = 0
  
  // Show dropdown if there are results
  if (filteredDomains.value.length > 0) {
    showDomainDropdown.value = true
  }
}

function filterSubdomains() {
  if (!subdomainInput.value) {
    filteredSubdomains.value = []
    return
  }

  if (!fuseSubdomains) return // Safety check

  const results = fuseSubdomains.search(subdomainInput.value)
  
  // If domain is selected, filter by that domain, otherwise show all
  const matches = selectedDomain.value 
    ? results.filter(r => r.item.domain === selectedDomain.value)
    : results
    
  filteredSubdomains.value = matches.map(r => r.item.subdomain).slice(0, 5)
  selectedSubdomainIndex.value = 0
  
  // Show dropdown if there are results
  if (filteredSubdomains.value.length > 0) {
    showSubdomainDropdown.value = true
  }
}

function selectDomain(index = selectedDomainIndex.value) {
  if (index < 0 || index >= filteredDomains.value.length) return
  
  selectedDomain.value = filteredDomains.value[index]
  domainInput.value = selectedDomain.value
  showDomainDropdown.value = false
  
  // Clear subdomain when domain changes
  subdomainInput.value = ''
  filteredSubdomains.value = []
}

function selectSubdomain(index = selectedSubdomainIndex.value) {
  if (index < 0 || index >= filteredSubdomains.value.length) return
  
  subdomainInput.value = filteredSubdomains.value[index]
  showSubdomainDropdown.value = false
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

function handleDomainBlur() {
  // Small delay to allow click events on dropdown items
  setTimeout(() => {
    showDomainDropdown.value = false
  }, 200)
}

function handleSubdomainBlur() {
  // Small delay to allow click events on dropdown items
  setTimeout(() => {
    showSubdomainDropdown.value = false
  }, 200)
}

// untouched by request
async function submitSelection() {
  const domain = domainInput.value.trim()
  const subdomain = subdomainInput.value.trim()

  if (!domain && !subdomain) {
    resultText.value = 'Please select domain and/or subdomain.'
    return
  }
  isLoading.value = true

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
  finally {
    isLoading.value = false
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
  box-sizing: border-box;
}

.typeaface-container {
  display: flex;
  flex-direction: row;
  font-size: clamp(0.75rem, 0.1843rem + 2.4465vw, 1.75rem);
  gap: 1vw;
  width: 100%;
  max-width: 500px;
  justify-content: center;
}

.domain-box, .subdomain-box {
  position: relative;
  width: 50%;
  max-width: 240px;
}

.domainInput, .subdomainInput {
  color: white;
  border: 2px solid #8707ff;
  border-radius: 10px;
  padding: 10px 25px;
  background: transparent;
  font-size: clamp(0.75rem, 0.3257rem + 1.8349vw, 1.5rem);
  width: 100%;
  box-sizing: border-box;
  outline: none;
}

.domainInput:active, .domainInput:focus {
  box-shadow: 2px 2px 15px #8707ff inset;
}

.subdomainInput:active, .subdomainInput:focus {
  box-shadow: 2px 2px 15px #8707ff inset;
}

.dropdown-wrapper {
  position: relative;
  width: 100%;
  z-index: 100;
}

.dropdown-list {
  list-style-type: none;
  margin: 0;
  padding: 0;
  border: 2px solid #8707ff;
  border-radius: 10px;
  background: black;
  color: white;
  overflow: hidden;
  box-shadow: 0 0 10px #8707ff55;
  position: absolute;
  z-index: 100;
  width: 100%;
  box-sizing: border-box;
  top: 5px;
  max-height: 200px;
  overflow-y: auto;
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
  width: 100%;
}

.submit-button {
  cursor: pointer;
  font-size: clamp(0.75rem, 0.6439rem + 0.4587vw, 0.9375rem);
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
  width: 100%;
}
/* From Uiverse.io by alexruix */ 
.loader {
  width: 48px;
  height: 48px;
  margin: auto;
  position: relative;
}

.loader:before {
  content: '';
  width: 48px;
  height: 5px;
  background: #f0808050;
  position: absolute;
  top: 60px;
  left: 0;
  border-radius: 50%;
  animation: shadow324 0.5s linear infinite;
}

.loader:after {
  content: '';
  width: 100%;
  height: 100%;
  background: #f08080;
  position: absolute;
  top: 0;
  left: 0;
  border-radius: 4px;
  animation: jump7456 0.5s linear infinite;
}

@keyframes jump7456 {
  15% {
    border-bottom-right-radius: 3px;
  }

  25% {
    transform: translateY(9px) rotate(22.5deg);
  }

  50% {
    transform: translateY(18px) scale(1, .9) rotate(45deg);
    border-bottom-right-radius: 40px;
  }

  75% {
    transform: translateY(9px) rotate(67.5deg);
  }

  100% {
    transform: translateY(0) rotate(90deg);
  }
}

@keyframes shadow324 {

  0%,
    100% {
    transform: scale(1, 1);
  }

  50% {
    transform: scale(1.2, 1);
  }
}
</style>
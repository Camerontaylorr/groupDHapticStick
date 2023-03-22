import EddystoneBeaconScanner from '@abandonware/eddystone-beacon-scanner'

const filters = [
  'fbe2f9bfa973'  // Put your second microbit ID in this string
]

const thresholds = {
  close: 25,
  medium: 50,
  far: Infinity
}

let currentMicrobitIndex = 0
let distances = [null, null]

EddystoneBeaconScanner.on('updated', (beacon) => {
  if (!filters.includes(beacon.id)) return
 
  const distance = Math.trunc(beacon.distance * 10)

  if (beacon.id === filters[currentMicrobitIndex]) {
    distances[currentMicrobitIndex] = distance
    const distanceText = getDistanceText(distance)
    console.log(`Microbit ${currentMicrobitIndex + 1} distance: ${distanceText}`)
   
    if (distance === 0) {
      currentMicrobitIndex++
    }
   
    if (currentMicrobitIndex >= filters.length) {
      console.log('You have arrived!')
      EddystoneBeaconScanner.stopScanning()
    }
  }
})

function getDistanceText(distance) {
  for (const [text, threshold] of Object.entries(thresholds)) {
    if (distance <= threshold) {
      return text
    }
  }
}

EddystoneBeaconScanner.startScanning(true)

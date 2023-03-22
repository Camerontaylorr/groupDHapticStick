import EddystoneBeaconScanner from '@abandonware/eddystone-beacon-scanner'

const filter = [
    ''  // Put your ID in this string
]

EddystoneBeaconScanner.on('updated', (beacon) => {
    if (filter.join() && !filter.includes(beacon.id)) return
    console.log('Updated: ' + beacon.id + ' - ' + beacon.url);
});

EddystoneBeaconScanner.startScanning(true)

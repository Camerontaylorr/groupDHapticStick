
import EddystoneBeaconScanner from '@abandonware/eddystone-beacon-scanner'

//filter for strings to be detected
const filter = [
    ''  // Put ID's in this string
]

EddystoneBeaconScanner.on('updated', (beacon) => {
    //check if filter has anything inside 
    if (filter.join() && !filter.includes(beacon.id)) return
    //print beacon url and id
    console.log('Updated: ' + beacon.id + ' - ' + beacon.url);
});

//start scanning for eddystone beacons
EddystoneBeaconScanner.startScanning(true)

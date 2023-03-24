import EddystoneBeaconScanner from '@abandonware/eddystone-beacon-scanner';
EddystoneBeaconScanner.on('updated', (beacon) => {
  console.log(`${beacon.id},${beacon.distance}`)

});
EddystoneBeaconScanner.startScanning(true);

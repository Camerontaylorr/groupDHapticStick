//import the EddystoneBeaconScanner module
import EddystoneBeaconScanner from '@abandonware/eddystone-beacon-scanner';

//set up a listener for the updated'event from the scanner
EddystoneBeaconScanner.on('updated', (beacon) => {
  //log the beacon's ID and distance to the console
  console.log(`${beacon.id},${beacon.distance}`)

});
//start scanning for the Eddystone beacons 
EddystoneBeaconScanner.startScanning(true);

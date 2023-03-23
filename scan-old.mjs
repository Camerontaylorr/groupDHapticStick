import EddystoneBeaconScanner from '@abandonware/eddystone-beacon-scanner';
import { spawn } from 'child_process';

const filters = [
    'fbe2f9bfa973',  // Put your first microbit ID in this string
    'f13efda77196',
];

const thresholds = {
  close: 25,
  medium: 50,
  far: Infinity,
};

let currentMicrobitIndex = 0;
let distances = [null, null];

function runPythonProcess() {
  const pythonProcess = spawn('python3', ['/home/pi/groupProject/main.py']);


  pythonProcess.stdout.on('data', (data) => {
    console.log(`ID is: ${data}`);
    console.log(parseInt(data))
    if (parseInt(data) === 584189697976) {
      currentMicrobitIndex++;
      distances = [null, null];
      console.log(`Moving to microbit ${currentMicrobitIndex + 1}`);
    } else if (parseInt(data) === 584189995784) {
      currentMicrobitIndex = 2;
      distances = [null, null, null];
      console.log(`Moving to microbit ${currentMicrobitIndex + 1}`);
    }
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Error from Python: ${data}`);
  });

  pythonProcess.on('close', (code) => {
    console.log(`Python process exited with code ${code}`);
    //runPythonProcess(); // spawn a new child process
  });

EddystoneBeaconScanner.on('updated', (beacon) => {
  if (!filters.includes(beacon.id)) return;


  const distance = Math.trunc(beacon.distance * 10);

  if (beacon.id === filters[currentMicrobitIndex]) {
    distances[currentMicrobitIndex] = distance;
    const distanceText = getDistanceText(distance);
    console.log(`Room ${currentMicrobitIndex + 1} distance: ${distanceText}`);

    if (distance === 0) {
      console.log(`Reached microbit ${currentMicrobitIndex + 1}`);
      runPythonProcess();
    }
  }
});

function getDistanceText(distance) {
  for (const [text, threshold] of Object.entries(thresholds)) {
    if (distance <= threshold) {
      return text;
    }
  }
}
}

runPythonProcess(); // start the first child process
EddystoneBeaconScanner.startScanning(true);
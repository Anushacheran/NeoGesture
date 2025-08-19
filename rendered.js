const { spawn } = require('child_process');
const path = require('path');

const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');

let processHandle;

startBtn.addEventListener('click', () => {
    if (!processHandle) {
        // Absolute path to your Python script
        const scriptPath = path.join(__dirname, 'gesturecontrol', 'gesture_control.py');

        // Spawn Python script (Windows-friendly using 'py' first, fallback to 'python')
        processHandle = spawn('py', [scriptPath]);

        processHandle.stdout.on('data', (data) => {
            console.log(`[Python stdout]: ${data}`);
        });

        processHandle.stderr.on('data', (data) => {
            console.error(`[Python stderr]: ${data}`);
        });

        processHandle.on('close', (code) => {
            console.log(`Python script exited with code ${code}`);
            processHandle = null;
        });

        processHandle.on('error', (err) => {
            console.error('Failed to start Python script:', err);
            // Fallback attempt with 'python'
            processHandle = spawn('python', [scriptPath]);
        });

        alert("Gesture Control Started");
    } else {
        alert("Gesture Control is already running!");
    }
});

stopBtn.addEventListener('click', () => {
    if (processHandle) {
        processHandle.kill();
        processHandle = null;
        alert("Gesture Control Stopped");
    } else {
        alert("No running process to stop.");
    }
});

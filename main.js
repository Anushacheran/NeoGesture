const { app, BrowserWindow } = require('electron');
const path = require('path');

let win;  // Keep a global reference to prevent garbage collection

function createWindow() {
    win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    win.loadFile('index.html');

    // Optional: Open DevTools for debugging
    // win.webContents.openDevTools();

    // Handle window closed
    win.on('closed', () => {
        win = null;
    });
}

// App ready
app.whenReady().then(createWindow);

// Quit when all windows are closed (except macOS)
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

// On macOS, recreate window when dock icon is clicked
app.on('activate', () => {
    if (win === null) {
        createWindow();
    }
});

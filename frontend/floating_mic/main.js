const { app, BrowserWindow, ipcMain,screen } = require('electron');
const path = require('path');
const { spawn } = require('child_process'); // To run external scripts

let activePythonProcess = null;

function createWindow() {
  const { width: screenWidth, height: screenHeight } = screen.getPrimaryDisplay().workAreaSize;
    // Set the window size to roughly match orbRig size
  const winWidth = 250;
  const winHeight = 250;
  const win = new BrowserWindow({
    width: winWidth,
    height: winHeight,
    x: screenWidth - winWidth, // Bottom-left X
    y: (screenHeight - winHeight), // Bottom-left Y (top-left origin)
    transparent: true,
    frame: false,
    alwaysOnTop: true,
    resizable: false,
    hasShadow: false,
    webPreferences: {
      contextIsolation: true,
      preload: __dirname + '/preload.js' // if you use preload
    }
  });

  win.loadFile('index.html');
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// Listen for the 'run-backend' message from the renderer (index.html)
ipcMain.handle('run-backend', () => {
  console.log('Main Process: Received request to run backend.');
  
  const pythonScriptPath = path.join(__dirname, '..', '..', 'Backend', 'main.py');
  const pythonVenvPath = path.join(__dirname, '..', '..', 'Backend', 'venv', 'Scripts', 'python.exe');
  const backendWorkingDirectory = path.join(__dirname, '..', '..', 'Backend');

  return new Promise((resolve, reject) => {
    
    // Check if a process is already running
    if (activePythonProcess) {
      console.warn("Backend process already running.");
      return reject(new Error("Process already running."));
    }

    const spawnEnv = { ...process.env, PYTHONUTF8: '1' };

    // --- STORE THE PROCESS ---
    activePythonProcess = spawn(
      pythonVenvPath, 
      ['-u', pythonScriptPath],
      { 
        env: spawnEnv,
        cwd: backendWorkingDirectory 
      }
    );

    activePythonProcess.stdout.on('data', (data) => {
      console.log(`KAI Backend: ${data}`);
    });

    activePythonProcess.stderr.on('data', (data) => {
      console.error(`KAI Backend Error: ${data}`);
    });

    activePythonProcess.on('close', (code) => {
      console.log(`Backend process exited with code ${code}`);
      activePythonProcess = null; // --- CLEAR THE PROCESS ---
      if (code === 0 || code === null) {
        resolve();
      } else {
        reject(new Error(`Backend process failed with code ${code}`));
      }
    });

    activePythonProcess.on('error', (err) => {
      console.error(`SPAWN ERROR: ${err.message}`);
      activePythonProcess = null; // --- CLEAR THE PROCESS ---
      reject(err);
    });
  });
});

// --- ADD THIS NEW LISTENER ---
// This listens for the 'stop' signal from the frontend
ipcMain.on('stop-backend-and-quit', () => {
  console.log('Main Process: Received request to STOP backend and QUIT.');
  
  if (activePythonProcess) {
    try {
      console.log('Killing active backend process...');
      activePythonProcess.kill(); // Send kill signal to the Python process
      activePythonProcess = null;
    } catch (e) {
      console.error("Failed to kill process:", e);
    }
  }
  
  console.log('Quitting Electron app...');
  app.quit(); // Quit the entire Electron application
});
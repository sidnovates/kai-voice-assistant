// preload.js

const { contextBridge, ipcRenderer } = require('electron');

// We are exposing a secure API to the renderer (index.html)
contextBridge.exposeInMainWorld('electron', {
  
  // This is the function you were already using
  runBackend: () => ipcRenderer.invoke('run-backend'),

  // --- ADD THIS ---
  // This is the new function to stop the backend and quit
  stopBackendAndQuit: () => ipcRenderer.send('stop-backend-and-quit')

});
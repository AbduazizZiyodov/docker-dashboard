const { app, BrowserWindow } = require("electron");

const url = require("url");
const path = require("path");

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1500,
    height: 850,
    maxWidth: 1500,
    maxHeight: 850,
    resizable: false,
    autoHideMenuBar: true,
    webPreferences: {
      nodeIntegration: true,
      devTools: false,
      spellcheck: false,
    },
  });
  console.log(path.join(__dirname, `index.html`));
  mainWindow.loadURL(
    url.format({
      pathname: path.join(__dirname, `index.html`),
      protocol: "file:",
      slashes: true,
    })
  );

  mainWindow.on("closed", function () {
    mainWindow = null;
  });
}

app.on("ready", createWindow);

app.on("window-all-closed", function () {
  if (process.platform !== "darwin") app.quit();
});

app.on("activate", function () {
  if (mainWindow === null) createWindow();
});

sudo apt-get remove docker-dashboard -y
rm -rf builds/

ng build

cp package.json builds/docker-dashboard-ng-build/ &&
    cp src/main.js builds/docker-dashboard-ng-build/

electron-packager builds/docker-dashboard-ng-build docker-dashboard --overwrite --asar \
    --platform=linux --arch=x64 \
    --prune=true --icon=src/icon.ico \
    --out=builds/

node installer.js

sudo dpkg -i builds/docker-dashboard_1.0.0_amd64.deb

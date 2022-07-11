PACKAGE="docker-dashboard"
STATUS=$(dpkg-query -W --showformat='${Status}\n' $PACKAGE | grep "install ok installed")

if [ "install ok installed" = "$STATUS" ]; then
  sudo apt-get remove $PACKAGE -y
fi

rm -rf builds/

ng build

cp package.json builds/docker-dashboard-ng-build/ &&
  cp src/main.js builds/docker-dashboard-ng-build/

electron-packager builds/docker-dashboard-ng-build docker-dashboard --overwrite --asar \
  --platform=linux --arch=x64 \
  --prune=true --icon=src/icon.ico \
  --out=builds/

node installer.js

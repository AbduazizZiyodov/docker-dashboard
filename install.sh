echo -e 'Installing supervisor ...\n'
sleep 1
sudo apt update && sudo apt install supervisor

sudo rm -rf src/env/ &&
    sudo rm -rf /usr/lib/docker-dashboard/ &&
    sudo rm -rf /etc/supervisor/conf.d/docker_dashboard.conf

cd src/server

echo -e '\nInstalling requirements for API(python) ...\n'
sleep 1
sudo pip3 install -r requirements.txt --no-cache

cd .. && cd ..

sudo mkdir /usr/lib/docker-dashboard && sudo mkdir /usr/lib/docker-dashboard/server

sudo cp -r src/server /usr/lib/docker-dashboard

sudo cp config/docker_dashboard.conf /etc/supervisor/conf.d/

echo -e '\nRestarting supervisor ...\n'
sleep 1
sudo systemctl restart supervisor

echo """
#################################################
#     ____          _                           #
#     |    \ ___ ___| |_ ___ ___                #
#     |  |  | . |  _| '_| -_|  _|               #
#     |____/|___|___|_,_|___|_|                 #           
#     ____          _   _                 _     #
#     |    \ ___ ___| |_| |_ ___ ___ ___ _| |   #
#     |  |  | .'|_ -|   | . | . | .'|  _| . |   #
#     |____/|__,|___|_|_|___|___|__,|_| |___|   #
#                                               #
#             By Abduaziz Ziyodov               #
#                                               #
#                 INSTALLED !!!                 #
#                                               #
#        API URL -> http://127.0.0.1:2121       #
#  SUPERVISOR STATUS -> http://127.0.0.1:9001   #
#################################################                 
"""

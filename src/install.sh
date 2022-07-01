clear
pip uninstall docker_dashboard -y


python3 setup.py sdist bdist_wheel && cd dist/
pip3 install docker_dashboard-1.0.0-py3-none-any.whl

cd ..
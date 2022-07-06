import sys

DOCKER_DASHBOARD_BANNER: str = """
    [bold cyan]     ____          _                        
        |    \ ___ ___| |_ ___ ___             
        |  |  | . |  _| '_| -_|  _|            
        |____/|___|___|_,_|___|_|                         
        ____          _   _                 _  
        |    \ ___ ___| |_| |_ ___ ___ ___ _| |
        |  |  | .'|_ -|   | . | . | .'|  _| . |
        |____/|__,|___|_|_|___|___|__,|_| |___|

            [bold green]Installed successfully :fire: 
    [bold cyan]Supervisor status :arrow_right: http://localhost:9001    
         [bold magenta]API url :arrow_right: http://localhost:2121     
"""

CURRENT_PATH: str = ""

OS: str = sys.platform
PYTHON_INTERPRETER: str = sys.executable
APP_INSTALL_PATH: str = "/usr/lib/docker-dashboard"
SUPERVISOR_CONFIG_PATH: str = "configs/docker_dashboard.conf"
ALL_COMPONENTS = [
    'requirements.txt',
    '__init__.py',
    'manage.py',
    'handlers.py',
    'containers',
    'images'
]

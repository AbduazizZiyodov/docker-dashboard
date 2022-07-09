# Super installer XD
import os
import sys
import shutil
import subprocess
import typing as t
from rich import print

import configs.installer_config as installer_config

NoneType = type(None)
installer_config.CURRENT_PATH = os.getcwd()


def print_error(message: str):
    print(f"[bold red]:x: Error {message}")
    sys.exit()


def print_success(message: str):
    print(f"[bold green]:white_check_mark: {message}")


def print_info(message: str):
    print(f"\n[bold cyan]:dizzy: {message}")


def check_supervisor() -> None:
    print_info("Checking supervisor ...")
    try:
        __import__("supervisor")
        print_success("Supervisor installed :rocket:")
    except ImportError:
        result = input(
            "The `supervisor` is not installed, can I install it? (y/n): ")

        if result.lower() == "y":
            print_info("Installing supervisor ...")
            run_command("sudo apt-get install supervisor -y")
            return
        print_error("Supervisor is not installed!")


def check_files() -> bool:
    run_command("rm -rf /usr/lib/docker-dashboard/")  # clear files ...
    print_info("Checking files ...")
    if "src" not in os.listdir():
        print_error("File checking - failed ... (src/ ?)")

    files = os.listdir("src/server")
    if all([
        component in files
        for component in installer_config.ALL_COMPONENTS
    ]):
        print_success("File checking - done!")
        return
    print_error("File checking - failed ...")


def run_command(command: str) -> t.Union[subprocess.CompletedProcess, NoneType]:
    result: subprocess.CompletedProcess = subprocess.run(
        command, shell=True, capture_output=True
    )

    if not result.stderr:
        return result

    error_message: str = result.stderr.decode("utf-8")
    print_error(error_message)


def copy_files():
    print_info("Copying server files ...")
    SERVER_DIR: str = f"{installer_config.APP_INSTALL_PATH}/server"

    shutil.copytree(
        f"{installer_config.CURRENT_PATH}/src/server", SERVER_DIR
    )

    shutil.copy(
        f"{installer_config.CURRENT_PATH}/{installer_config.SUPERVISOR_CONFIG_PATH}",
        "/etc/supervisor/conf.d/"
    )

    os.chdir(installer_config.APP_INSTALL_PATH)
    print_success("Files copied!")


def create_venv():
    print_info("Creating virtual environment ...")
    run_command(f"{installer_config.PYTHON_INTERPRETER} -m venv env")
    print_success("Virtual environment created!")

    if 'env' in os.listdir():
        run_command(". env/bin/activate")
        print_success('Virtual environment activated!')
        return

    print_error("While creating a virtual environment")


def install_dependencies():
    PYTHON: str = installer_config.PYTHON_INTERPRETER.split("/")[-1]
    install_command: str = f"{installer_config.APP_INSTALL_PATH}/env/bin/{PYTHON} -m pip install -r server/requirements.txt"
    if "requirements.txt" in os.listdir("server"):
        print_info("Installing python dependencies ...")
        run_command(install_command)
        print_success("Python dependencies are installed!")
        return

    print_error("requirments.txt not found (server/requirements.txt ?)")


def restart_supervisor():
    run_command("systemctl restart supervisor")


def install_debian_package():
    os.chdir(installer_config.CURRENT_PATH)
    run_command(f"sudo dpkg -i {installer_config.DEBIAN_PACKAGE}")


def main():
    check_supervisor()
    check_files()
    copy_files()
    create_venv()
    install_dependencies()
    restart_supervisor()
    install_debian_package()
    print(installer_config.DOCKER_DASHBOARD_BANNER)


if __name__ == "__main__":
    main()

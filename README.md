# 🐳 **Docker Dashboard**

> **_Simple lightweight GUI application for working with Docker!_**

Perhaps it can be a good alternative to Docker Desktop in the future 😂

## **📄 Requirements**:

- Python **+3.8**
- Operating system: `ubuntu` (tested `20.04 LTS`, `22.04 LTS`).

## **📦 Installation**

Go to the [releases](https://github.com/AbduazizZiyodov/docker-dashboard/releases). Download the latest version (`docker-dashboard-*.tar.gz`) and extract archive.

```bash
$ mkdir docker-dashboard/
$ tar -xf docker-dashboard-*.tar.gz -C docker-dashboard/
```

Open the directory on the terminal and run this command:

```bash
$ cd docker-dashboard/
$ sudo ./install.sh
```
![](/assets/install.png)

- **Supervisor status**:
  ![](/assets/supervisor_status.png)

- **API status**:
  ![](/assets/api_status.png)



## **🔧 Development**

Clone this repository

```bash
$ git clone https://github.com/AbduazizZiyodov/docker-dashboard
```

**Running 🚀**

- `backend` (from src/):
  ```bash
  $ uvicorn server.asgi:application --reload --port 2121 # install dependencies from requirements.txt
  ```
- `tests` (from src/server/)
  ```bash
  $ pytest # test_requirements.txt
  ```
- `frontend` (from src/client)
  ```bash
  $ npm start # or ng serve (global)
  ```

## **🏗️ Build**

First, you have to install some system dependencies,`rust` and `cargo`

**Install system dependencies**

```bash
$ sudo apt update
$ sudo apt install libwebkit2gtk-4.0-dev \
    build-essential \
    curl \
    libssl-dev \
    libgtk-3-dev \
    libayatana-appindicator3-dev \
    librsvg2-dev
```

**Install rust 🦀**

```bash
$ curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh
$ rustup update # for updating
```

**Install cargo📦**

```bash
$ sudo apt install cargo
```

### **🧮 Commands**

For testing client-side. You can view, or fix something.

```bash
$ cargo tauri dev
```

Build client-side. You should check `src/client/src-tauri/target` folder.

```bash
$ cargo tauri build
```

## **🧪 Testing**

Used `pytest`, (tests -> src/server/tests)

```bash
$ cd src/server
$ pytest
```

![](/assets/tests.png)

<hr>

<p align='center'>
    Author: <strong>Abduaziz Ziyodov</strong> 
</p>

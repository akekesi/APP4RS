# APP4RS
<div align="center">

   [![Status](https://img.shields.io/badge/Status-in_progress-yellow.svg)](https://github.com/akekesi/connect4?tab=readme-ov-file#description)
   [![CI](https://github.com/akekesi/APP4RS/actions/workflows/ci.yml/badge.svg)](https://github.com/akekesi/APP4RS/actions)
</div>

<div align="center">

   [![Python](https://img.shields.io/badge/Python-3.12.7-blue)](https://www.python.org/downloads/release/python-3127/)
</div>

<!-- <p align="center">
   <a href="#demo" title="Click to view full-size GIF in Demo section">
      <img src="???" alt="???">
  </a>
</p> -->

## Table of Contents
1. [Description](#description)
1. [Demo](#demo)
1. [Prerequisites](#prerequisites)
1. [Python Installation (WSL Ubuntu)](#python-installation-wsl-ubuntu)
1. [Poetry Installation (WSL Ubuntu)](#poetry-installation-wsl-ubuntu)
1. [Usage Poetry Shell (WSL Ubuntu)](#usage-poetry-shell-wsl-ubuntu)
1. [Usage](#usage)
1. [Results](#results)
1. [To-Do](#to-do)
1. [Authors](#authors)
1. [Acknowledgements](#acknowledgements)
1. [License](#license)

## Description
🚧 This project is a work in progress. Some features may be incomplete, untested, or lacking full documentation. 🚧  

This project was initially developed as an assignment for the [TU Berlin Advanced Python Programming for Deep Learning in Remote Sensing (APP4RS) [WiSe 2024/25]](https://isis.tu-berlin.de/course/view.php?id=39563).

## Prerequisites
- [Python 3.12.7](https://www.python.org/downloads/release/python-3127/)
- [Poetry](https://python-poetry.org/docs/)

## Python Installation (WSL Ubuntu)
### 1. Update Your Package List
```bash
$ sudo apt update
$ sudo apt upgrade
```
### 2. Install Required Dependencies
```bash
$ sudo apt install software-properties-common
```
### 3. Add the Deadsnakes PPA
```bash
$ sudo add-apt-repository ppa:deadsnakes/ppa
$ sudo apt update
```
### 4. Install Python 3.12
```bash
$ sudo apt install python3.12
$ python3.13 --version
```
### 5. Set Python 3.12 as the Default Python 3 Version
```bash
$ sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1
$ python3 --version
```
### 6. Install pip for Python 3.12
```bash
$ sudo apt install python3.12-distutils
$ curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12
$ pip3 --version
```

## Poetry Installation (WSL Ubuntu)
### 1. Install Poetry
```bash
$ curl -sSL https://install.python-poetry.org | python3 -
$ poetry --version
```
### 2. Create a New Poetry Project
```bash
$ cd projects
$ poetry new <project_name>
```
### 3. Configure Dependencies
```toml
[tool.poetry]
name = "task-1-remote-sensing-data"
version = "0.1.0"
description = ""
authors = ["Attila Kekesi <kekesi.att@gmail.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.12"
numpy = ">=2.1.0"
pandas = ">=2.2.0"
pyarrow = ">=17.0.0"
duckdb = ">=1.1.0"
polars = ">=1.8.0"
geopandas = ">=1.0.0"
rasterio = ">=1.4.0"
rioxarray = ">=0.17.0"
geocube = ">=0.7.0"
folium = ">=0.16.0"
matplotlib = ">=3.9.0"
dask = ">=2024.9.0"
ray = ">=2.36.0"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```
### 4. Install Dependencies
```bash
$ cd projects/<project_name>
$ poetry install
```
### 5. Verify the Lock File
Check that the `poetry.lock` file has been created in your project directory and contains the correct libraries and versions.
```bash
$ poetry show --tree
$ poetry check
```

## Usage Poetry Shell (WSL Ubuntu)
### 1. Activate the Virtual Environment
```bash
$ poetry shell
```
### 2. Dectivate the Virtual Environment
```bash
$ exit
```
or
```bash
$ deactivate
```

## Usage
### Links
- [APP4RS - ISIS](https://isis.tu-berlin.de/course/view.php?id=39563)
- [APP4RS - GitHub akekesi](https://github.com/akekesi/APP4RS)
- [APP4RS - GitLab TU Berlin](https://git.tu-berlin.de/rsim/app4rs/APP4RS_WiSe24_Group01)
- [APP4RS - Result](https://ntfy.app4rs.org/APP4RS_WiSe24_Group01_63e4a218e97f5bf97bd498c99288a237)

## Results
### 1. **eed4f9160d211872c259a7f1f0399c8cfe2b0eb0:**
```bash
$ python main.py
spring: 0
summer: 4950
fall: 0
winter: 0
average-num-labels: 3.58
maximum-num-labels: 9
wrong-size: 125
with-no-data: 849
not-part-of-dataset: 50
B01 mean: 217
B01 std-dev: 138
B02 mean: 293
B02 std-dev: 185
B03 mean: 465
B03 std-dev: 251
B04 mean: 354
B04 std-dev: 319
B05 mean: 724
B05 std-dev: 442
B06 mean: 1787
B06 std-dev: 997
B07 mean: 2152
B07 std-dev: 1214
B08 mean: 2316
B08 std-dev: 1333
B8A mean: 2355
B8A std-dev: 1327
B09 mean: 2353
B09 std-dev: 1290
B11 mean: 1330
B11 std-dev: 834
B12 mean: 749
B12 std-dev: 579
geom-average-num-labels: 2.10
geom-num-overlaps: 4981
```

## To-Do
### Notation
- [ ] Task to do
- [x] Task in progress
- [x] ~~Task finished~~

### To-Do
- [ ] Using [GitHub Issues](https://github.com/akekesi/Connect4/issues) insted of this To-Do list 😎
- [ ] Add coverage as dev
- [ ] Add pylint as dev
- [ ] Add logging
- [ ] Add version
- [ ] Add badges (GitHub Actions CI)
- [ ] Add badges (GitHub Actions Coverage)
- [ ] Add badges (Version)
- [ ] Add badges (...)
- [ ] Add demo, animation, or video
- [ ] Complete README.md
- [ ] Update CI.yml [(deprecation of v3 of the artifact actions)](https://github.blog/changelog/2024-04-16-deprecation-notice-v3-of-the-artifact-actions/)

## Authors
Attila Kékesi

## Acknowledgements
- [TU Berlin Advanced Python Programming for Deep Learning in Remote Sensing (APP4RS) [WiSe 2024/25]](https://isis.tu-berlin.de/course/view.php?id=39563).

## License
Code released under the [MIT License](https://github.com/akekesi/APP4RS/blob/main/LICENSE).

# Certoratomation
## Automation Framework For Frontend

### Packages and prerequisites

- [Git](https://git-scm.com/downloads)
- Pip
- Python3.11
- playwright
- [Poetry](https://python-poetry.org/docs/)
- [NodeJS](https://nodejs.org/en/download) (latest?)

### Downloads and installation

- Create root folder - '/path/to/local/folder/ROOT_FOLDER_EXAMPLE'
- Navigate inside folder 
  - 'cd ROOT_FOLDER_EXAMPLE'
######
- Clone FE to root folder 
  - 'git clone -b main git@github.com:Certora/new_report.git'
######
- Clone automation project to root folder 
  - 'git clone -b main git@github.com:yoav-el-certora/certoratomation.git'
  - Navigate inside automation project - 'cd certoratomation'
  - Init submodules - 'git submodule init ; git submodule update --recursive'
######
- Install Framework
  - 'poetry lock ; poetry install'
  - 'playwright install'
######
- Folder structure should be as follows:
  - ROOT_FOLDER_EXAMPLE
    - certoratomation
      - certoratomation
      - DevUtils
      - tests
      - tests_local_resources
    - new_report


### Running Server/CI

- Navigate to certoratomation folder
- Run 'poetry run python3 certoratomation -h' for options.
- Run 'poetry run python3 certoratomation --run_server' to init local server for API communication.
- Run 'poetry run python3 certoratomation --run_ci' to execute all CI tests.



### Recommended IDE Setup

- [PyCharm](https://www.jetbrains.com/pycharm/download)

# ETL Project with Docker MySQL

## Description
A Python-based ETL (Extract, Transform, Load) project that demonstrates data manipulation and transfer between MySQL databases using Docker containers.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Development](#development)
- [Code Quality](#code-quality)
- [Future Improvements](#future-improvements)
- [License](#license)


## Features
- Docker-based MySQL database management
- Fake data generation using Faker
- Automated table creation with relationships
- Data transfer between databases
- Complex SQL query execution
- Object-oriented Python implementation
- Unit testing with pytest
- Code quality tools integration

## Prerequisites
- Python 3.12+
- Docker & Docker Compose
- Git

## Installation
1. Clone the repository
```bash
git clone https://github.com/yourusername/Projet-ETL-avec-Docker-MySQL.git
cd Projet-ETL-avec-Docker-MySQL
```

2. Create and activate virtual environment
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Start Docker containers
```bash
docker-compose up -d
```

## Project Structure
```
Projet-ETL-avec-Docker-MySQL/
├── core/                   # Core application code
│   ├── __init__.py
│   ├── create_tables.py   # Database table creation
│   ├── joboard_class.py   # Job board functionality
│   └── mysqlsource.py     # Database connection handling
├── tests/                 # Test files
│   ├── __init__.py
│   └── test_create_tables.py
├── docker/               # Docker configuration
│   └── docker-compose.yml
├── notebooks/           # Jupyter notebooks
│   └── jobboard_db.ipynb
├── docs/               # Documentation
│   └── etl_process.png
├── .pre-commit-config.yaml
├── requirements.txt
└── README.md
```


## Development
### Setup Development Environment
```bash
pip install -r requirements-dev.txt
pre-commit install
```

## Future Improvements
- [ ] FastAPI Implementation
  - REST API endpoints
  - Job recommendation system
  - OpenAPI documentation
- [ ] CI/CD Pipeline
- [ ] Enhanced Error Handling
- [ ] Logging System



## License
MIT License

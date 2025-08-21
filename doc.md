# ETL Project with Docker MySQL

## Description
A Python-based ETL (Extract, Transform, Load) project that demonstrates data manipulation and transfer between MySQL databases using Docker containers.

## Features
- Create and manage MySQL databases using Docker
- Generate fake data for testing using Faker
- Create tables with proper relationships and constraints
- Insert data into MySQL databases
- Copy data between databases
- Execute complex SQL queries
- Object-oriented implementation with Python classes

## Prerequisites
- Docker
- Python 3.x
- MySQL Connector/Python
- Faker library
- Pandas

## Installation
1. Clone the repository
```bash
git clone https://github.com/yourusername/mysql-docker-project.git
cd mysql-docker-project
```

2. Install required Python packages
```bash
pip install mysql-connector-python
pip install faker
pip install pandas
```

3. Start Docker containers
```bash
docker-compose up -d
```

## Project Structure
```
mysql-docker-project/
├── docker-compose.yml
├── joboard_class.py
├── joboard_functions.py
├── create_load_data.py
├── mysql-jupyter.ipynb
└── README.md
```

## Usage
1. Create databases and tables:
```python
python create_load_data.py
```

2. Generate and insert fake data:
```python
python joboard_class.py
```

## Database Schema
- Users (id, name, email, role)
- Companies (id, name, location)
- Categories (id, name)
- Jobs (id, title, description, location, company_id, category_id)
- Applications (id, user_id, job_id, cover_letter, date_applied)

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Authors 
- Your Name

## Acknowledgments
- MySQL Connector/Python documentation
- Faker library documentation
- Docker documentation
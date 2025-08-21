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


## Commit project
1. git status
2. git add .
3. git commit -m "your message"
4. git push origin main

5. git commit --amend -m "Nouveau message de commit" #Update a commit message
    git push --force origin main
 6. git clone url_report # Pour cloner le project
 7. git remote add origin git@github.com:TON-USER/NOM-DEPOT.git
 ##Other cmd
git remote -v                         # vérifier le remote
git log --oneline --graph --decorate  # historique compact
git pull --rebase origin main         # récupérer les derniers commits proprement
git branch -vv                        # voir les branches et suivi
git rm --cached chemin/fichier        # retirer du suivi Git (garde le fichier local)



1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


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
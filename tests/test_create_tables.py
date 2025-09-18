import pytest
from unittest.mock import MagicMock
import mysql.connector

from core.Create_tables import CreateTables


@pytest.fixture
def mock_cursor():
    """Fixture to create a mock MySQL cursor."""
    cursor = MagicMock()
    return cursor

@pytest.fixture
def create_tables(mock_cursor):
    """Fixture to create an instance of CreateTables with mock cursor."""
    return CreateTables(cursor=mock_cursor)

def test_create_user_table(create_tables, mock_cursor):
    """Test creation of user table."""
    create_tables.create_user_table()
    mock_cursor.execute.assert_called_once()
    call_args = mock_cursor.execute.call_args[0][0]
    assert "CREATE TABLE IF NOT EXISTS users" in call_args
    assert "id INT AUTO_INCREMENT PRIMARY KEY" in call_args
    assert "name VARCHAR(100)" in call_args
    assert "email VARCHAR(100)" in call_args
    assert "role VARCHAR(100)" in call_args

def test_create_company_table(create_tables, mock_cursor):
    """Test creation of company table."""
    create_tables.create_company_table()
    mock_cursor.execute.assert_called_once()
    call_args = mock_cursor.execute.call_args[0][0]
    assert "CREATE TABLE IF NOT EXISTS companies" in call_args
    assert "id INT AUTO_INCREMENT PRIMARY KEY" in call_args
    assert "name VARCHAR(255) NOT NULL" in call_args
    assert "location VARCHAR(255) NOT NULL" in call_args

def test_create_category_table(create_tables, mock_cursor):
    """Test creation of category table."""
    create_tables.create_category_table()
    mock_cursor.execute.assert_called_once()
    call_args = mock_cursor.execute.call_args[0][0]
    assert "CREATE TABLE IF NOT EXISTS categories" in call_args
    assert "id INT AUTO_INCREMENT PRIMARY KEY" in call_args
    assert "name VARCHAR(100) NOT NULL" in call_args

def test_create_job_table(create_tables, mock_cursor):
    """Test creation of job table."""
    create_tables.create_job_table()
    mock_cursor.execute.assert_called_once()
    call_args = mock_cursor.execute.call_args[0][0]
    assert "CREATE TABLE IF NOT EXISTS jobs" in call_args
    assert "id INT AUTO_INCREMENT PRIMARY KEY" in call_args
    assert "title VARCHAR(255) NOT NULL" in call_args
    assert "description TEXT NOT NULL" in call_args
    assert "FOREIGN KEY (company_id) REFERENCES companies(id)" in call_args
    assert "FOREIGN KEY (category_id) REFERENCES categories(id)" in call_args

def test_create_application_table(create_tables, mock_cursor):
    """Test creation of application table."""
    create_tables.create_application_table()
    mock_cursor.execute.assert_called_once()
    call_args = mock_cursor.execute.call_args[0][0]
    assert "CREATE TABLE IF NOT EXISTS applications" in call_args
    assert "id INT AUTO_INCREMENT PRIMARY KEY" in call_args
    assert "user_id INT" in call_args
    assert "job_id INT" in call_args
    assert "status VARCHAR(50) NOT NULL" in call_args
    assert "FOREIGN KEY (user_id) REFERENCES users(id)" in call_args
    assert "FOREIGN KEY (job_id) REFERENCES jobs(id)" in call_args

def test_cursor_error_handling(mock_cursor):
    """Test error handling when cursor operations fail."""
    mock_cursor.execute.side_effect = mysql.connector.Error("Database error")
    tables = CreateTables(cursor=mock_cursor)
    
    with pytest.raises(mysql.connector.Error):
        tables.create_user_table()







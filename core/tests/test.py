import pytest
from core.Mysqlsource import Mysqlsource

class TestMysqlsource:
    def test_connection(self):
        mysql = Mysqlsource(host='localhost', user='root', password='password', database='test_db')
        conn = mysql.connect()
        assert conn is not None


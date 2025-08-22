import mysql.connector

class ConnnectToDB:
    """Class to handle database connections and operations."""
    def __init__(self, host:str, port:int, user: str, password:str, database:str)-> None:
        """Initialize the database connection."""
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    def connect(self)-> tuple[str,str]|tuple[None,None]:
        """Connect to the database and return the connection and cursor."""
        try:
            connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            cursor = connection.cursor()
            print(f"✅ Connected to {self.database} database successfully")
            return connection, cursor
        except mysql.connector.Error as err:
            print(f"❌ Error: {err}")
            return None, None
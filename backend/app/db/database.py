"""
Database configuration and connection management
"""
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()


class DatabaseConfig:
    """Database configuration class"""
    
    HOST = os.getenv('DB_HOST', 'localhost')
    PORT = int(os.getenv('DB_PORT', 3306))
    USER = os.getenv('DB_USER', 'root')
    PASSWORD = os.getenv('DB_PASSWORD', 'Qwertghjkl$1')
    DATABASE = os.getenv('DB_NAME', 'employee_management')


class DatabaseConnection:
    """Database connection manager"""
    
    _instance = None
    _connection = None
    
    def __new__(cls):
        """Singleton pattern to ensure single database connection"""
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def get_connection(self):
        """Get database connection"""
        try:
            if self._connection is None or not self._connection.is_connected():
                self._connection = mysql.connector.connect(
                    host=DatabaseConfig.HOST,
                    port=DatabaseConfig.PORT,
                    user=DatabaseConfig.USER,
                    password=DatabaseConfig.PASSWORD,
                    database=DatabaseConfig.DATABASE
                )
                print("Database connection established successfully")
            return self._connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            raise
    
    def close_connection(self):
        """Close database connection"""
        if self._connection and self._connection.is_connected():
            self._connection.close()
            print("Database connection closed")


def get_db_connection():
    """Helper function to get database connection"""
    db = DatabaseConnection()
    return db.get_connection()


def initialize_database():
    """Initialize database and create tables if they don't exist"""
    try:
        # First, connect without specifying database to create it if needed
        connection = mysql.connector.connect(
            host=DatabaseConfig.HOST,
            port=DatabaseConfig.PORT,
            user=DatabaseConfig.USER,
            password=DatabaseConfig.PASSWORD
        )
        cursor = connection.cursor()
        
        # Create database if not exists
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DatabaseConfig.DATABASE}")
        print(f"Database '{DatabaseConfig.DATABASE}' created or already exists")
        
        cursor.close()
        connection.close()
        
        # Now connect to the specific database
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Create employees table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS employees (
            id INT AUTO_INCREMENT PRIMARY KEY,
            employee_id VARCHAR(50) UNIQUE NOT NULL,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            email VARCHAR(150) UNIQUE NOT NULL,
            phone VARCHAR(20),
            department VARCHAR(100),
            position VARCHAR(100),
            salary DECIMAL(10, 2),
            hire_date DATE,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_table_query)
        print("Employees table created or already exists")
        
        connection.commit()
        cursor.close()
        
        return True
    except Error as e:
        print(f"Error initializing database: {e}")
        return False
"""
Database Configuration Module
Handles database connections with environment variables and error handling
"""

import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


class DatabaseConfig:
    """Database configuration and connection management"""
    
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD')
        self.database = os.getenv('DB_NAME', 'healthcare_db')
        self.port = os.getenv('DB_PORT', '3306')
    
    def get_connection(self):
        """
        Create and return a database connection
        
        Returns:
            mysql.connector.connection: Database connection object
            
        Raises:
            Error: If connection fails
        """
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            
            if connection.is_connected():
                return connection
                
        except Error as e:
            raise Error(f"Error connecting to MySQL database: {e}")
    
    def test_connection(self):
        """
        Test the database connection
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            conn = self.get_connection()
            if conn.is_connected():
                db_info = conn.get_server_info()
                conn.close()
                return True, f"Successfully connected to MySQL Server version {db_info}"
        except Error as e:
            return False, f"Connection failed: {e}"


def get_db_connection():
    """
    Convenience function to get a database connection
    
    Returns:
        mysql.connector.connection: Database connection object
    """
    db_config = DatabaseConfig()
    return db_config.get_connection()


if __name__ == "__main__":
    # Test the connection
    db = DatabaseConfig()
    success, message = db.test_connection()
    print(message)

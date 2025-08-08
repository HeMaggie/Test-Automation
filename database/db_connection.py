import mysql.connector
from mysql.connector import Error
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DatabaseConnection:
    def __init__(self, hostname, username, password, db_name):
        self.connection = None
        self.cursor = None
        try:
            logger.info(f"Attempting to connect to database at {hostname}")
            self.connection = mysql.connector.connect(
                host=hostname,
                user=username,
                passwd=password,
                db=db_name,
                connect_timeout=10,
                autocommit=False
            )
            self.cursor = self.connection.cursor(dictionary=True)
            logger.info("Database connection established successfully")
        except Error as e:
            logger.error(f"Error connecting to database: {e}")
            self.connection = None
            raise Exception(f"Failed to connect to database: {e}")

    def execute_query(self, query, params=None):
        if not self.connection:
            logger.error("No database connection available")
            raise Exception("Database connection not available")
        
        try:
            logger.debug(f"Executing query: {query}")
            if params:
                self.cursor.execute(query, params)
                logger.debug(f"Query parameters: {params}")
            else:
                self.cursor.execute(query)
            self.connection.commit()
            logger.debug("Query executed successfully")
        except Error as e:
            logger.error(f"Error executing query: {e}")
            self.connection.rollback()
            raise Exception(f"Query execution failed: {e}")

    def fetch_results(self):
        if not self.connection:
            logger.error("No database connection available for fetching results")
            return []
        
        try:
            results = self.cursor.fetchall()
            logger.debug(f"Fetched {len(results)} rows")
            return results
        except Error as e:
            logger.error(f"Error fetching results: {e}")
            return []

    def close(self):
        try:
            if self.cursor:
                self.cursor.close()
                logger.debug("Database cursor closed")
            if self.connection and self.connection.is_connected():
                self.connection.close()
                logger.info("Database connection closed")
        except Error as e:
            logger.error(f"Error closing database connection: {e}")


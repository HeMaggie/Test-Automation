import MySQLdb
from MySQLdb.cursors import DictCursor

class DatabaseConnection:
	def __init__(self, hostname, username, password, db_name):
		self.connection = MySQLdb.connect(
			host=hostname,
			user=username,
			passwd=password,
			db=db_name,
			cursorclass=DictCursor
		)
		self.cursor = self.connection.cursor()

	def execute_query(self, query, params=None):
		if params:
			self.cursor.execute(query, params)
		else:
			self.cursor.execute(query)
		self.connection.commit()

	def fetch_results(self):
		return self.cursor.fetchall()

	def close(self):
		self.cursor.close()
		self.connection.close()
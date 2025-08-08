from database.db_connection import DatabaseConnection
from config import Config

class GetMypos(DatabaseConnection):
	def __init__(self, hostname=None):
		if hostname is None:
			hostname = Config.DB_HOST
		super().__init__(
			hostname, 
			username=Config.DB_USERNAME, 
			password=Config.DB_PASSWORD, 
			db_name=Config.DB_NAME
		)

	def get_mystore(self):
		q = "SELECT * FROM mystore"
		self.execute_query(q)
		results = self.fetch_results()
		return results

	def get_myorder(self, condition=None):
		q = f"SELECT * FROM myorder {condition}"
		self.execute_query(q)
		results = self.fetch_results()
		return results

	def get_cc(self):
		q = "SELECT * FROM cc"
		self.execute_query(q)
		results = self.fetch_results()
		return results

	def update_mystore_setting(self, setting, value):
		q = f'UPDATE mystore SET {setting} = %s'
		self.execute_query(q, (value,))

	def update_mystore_settings(self, setting_dict):
		set_clause = ','.join([f'{key} = %s' for key in setting_dict.keys()])
		q = f'UPDATE mystore SET {set_clause} '
		v = tuple(setting_dict.values())
		self.execute_query(q, v)
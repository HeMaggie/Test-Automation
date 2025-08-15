from database.db_connection_win_version import DatabaseConnection
from config import Config
import json

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
		# Check if setting contains underscore (indicates JSON field update)
		if '.' in setting:
			# Split setting into JSON column name and key
			parts = setting.split('.', 1)
			json_column = parts[0]  # e.g., "support"
			json_key = parts[1]      # e.g., "taxb4discountnew"
			
			# Get current JSON value from database
			q = f'SELECT {json_column} FROM mystore'
			self.execute_query(q)
			result = self.fetch_results()
			
			if result and len(result) > 0:
				# Parse existing JSON or create new dict
				current_json = result[0].get(json_column)
				if current_json:
					try:
						json_data = json.loads(current_json) if isinstance(current_json, str) else current_json
					except (json.JSONDecodeError, TypeError):
						json_data = {}
				else:
					json_data = {}
				
				# Update the specific key in JSON
				json_data[json_key] = value
				
				# Update the entire JSON column in database
				q = f'UPDATE mystore SET {json_column} = %s'
				self.execute_query(q, (json.dumps(json_data),))
		else:
			# Direct update for regular settings
			q = f'UPDATE mystore SET {setting} = %s'
			self.execute_query(q, (value,))

	def update_mystore_settings(self, setting_dict):
		# Handle each setting individually to support both regular and JSON updates
		for setting, value in setting_dict.items():
			self.update_mystore_setting(setting, value)
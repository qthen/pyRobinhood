'''
Responsible for loading environment constants that this package depends on.

Loads it's settings from the config/ dir or a supplied directory.
'''

import json

class ConfigService(object):

	'''
	Inputs:
		config_dir (String) - Filepath for the config dir.
	'''
	def __init__(self, config_dir="config/"):
		self.CONFIG_DIR = config_dir

	'''
	Gets the user info currently loaded in the config dir.
	Returns:
		(Dict) - User info
	'''
	def get_user_info(self):
		try:
			user_info_config_fp = self.CONFIG_DIR + "user_info.json"
			user_info_config_file = open(user_info_config_fp, 'r')
			user_info = json.load(user_info_config_file)
			user_info_config_file.close()
			return user_info
		except FileNotFoundError:
			raise FileNotFoundError("Unable to load user_info configs since user_info.json was not found")
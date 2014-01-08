class JsonParser:
	"""
	1. This class can read data in JSON format, and read/write data through DICT in Python.
	2. It can store data from a dict, update data in the instance, and transfer data to JSON.
	3. It provides a consistent way to transfer data.
	4. It provides methods to dump data to files and load it from files.
	"""
	def __init__(self):
		"""
		init
		"""
	def load(self, s):
		"""
		load string s in JSON format
		"""
	def dump(self):
		"""
		return a string in JSON format according to self.data
		"""
	def loadJson(self, f):
		"""
		load JSON data from file f
		"""
		with open(f) as mFile:
			self.json = mFile.read()
	def dumpJson(self, f):
		"""
		store self.data to file f in JSON format, if f exists then overwrite it
		"""
	def dumpDict(self, d):
		"""
		load data in d, regardless of the item whose key is not a string
		"""
	def dumpDict(self):
		"""
		return a dict according to self.data
		"""

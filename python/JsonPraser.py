import copy

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
		self.json = ''
		self.d = {}

	def load(self, s):
		"""
		load string s in JSON format
		"""
		self.json = s
		#TODO: transfer json to dict

	def dump(self):
		"""
		return a string in JSON format
		"""
		return self.json

	def loadJson(self, f):
		"""
		load JSON data from file f
		"""
		with open(f) as mFile:
			self.load(mFile.read())
		#TODO: transfer json to dict

	def dumpJson(self, f):
		"""
		store data to file f in JSON format, if f exists then overwrite it
		"""
		with open(f, w) as mFile:
			mFile.write(self.json)

	def loadDict(self, d):
		"""
		load data in d, regardless of the item whose key is not a string
		"""
		for key in d:
			if isinstance(key, str):
				self.d[key] = copy.deepcopy(d[key])
		#TODO: transfer dict to json

	def dumpDict(self):
		"""
		return a dict according to self.data
		"""
		return copy.deepcopy(d)

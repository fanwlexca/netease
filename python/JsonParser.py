# coding = utf-8
"""
Implementation of JsonParser
"""
import sys, copy

ESCAPE_DCT = {
		u'"' : '\\"',
		u'\\' : '\\\\',
		u'/' : '\\/',
		u'\b' : '\\b',
		u'\f' : '\\f',
		u'\n' : '\\n',
		u'\r' : '\\r',
		u'\t' : '\\t',
}

BACKSLASH = {
		'"' : '"', 
		'\\' : '\\',
		'/' : '/',
		'b' : '\b',
		'f' : '\f',
		'n' : '\n',
		'r' : '\r',
		't' : '\t',
}


class FormatError(Exception):
	"""
	FormatError Exception
	"""
	pass

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

	def __getitem__(self, key):
		"""
		using '[]' to read
		"""
		return self.d[key]

	def __setitem__(self, key, value):
		"""
		using '[]' to assign
		"""
		self.d[key] = value
		self.dictToJson()

	def load(self, s):
		"""
		load string s in JSON format
		"""
		self.json = s
		self.jsonToDict()

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
		self.jsonToDict()

	def dumpJson(self, f):
		"""
		store data to file f in JSON format, if f exists then overwrite it
		"""
		with open(f, 'w') as mFile:
			mFile.write(self.json)

	def loadDict(self, d):
		"""
		load data in d, regardless of the item whose key is not a string
		"""
		for key in d:
			if isinstance(key, unicode):
				self.d[key] = copy.deepcopy(d[key])
		self.dictToJson()

	def dumpDict(self):
		"""
		return a dict according to self.d
		"""
		return copy.deepcopy(self.d)

	def jsonToDict(self):
		"""
		transform json to dict
		"""
		s = self.json
		s = s.strip()
		if s[0] == '{' and s[-1] == '}':
			self.d = encodeObj(s)
		else:
			raise FormatError('Json format error: outermost layer must be object')

	def dictToJson(self):
		"""
		transform dict to json
		"""
		self.json = decodeObj(self.d)

	def update(self, d):
		"""
		update self.d according to d
		"""
		for key in d:
			if isinstance(key, unicode):
				self.d[key] = copy.deepcopy(d[key])
		self.dictToJson()

def encodeVal(value):
	"""
	encode each value
	"""
	value = value.strip()
	if value[0] == '{' and value[-1] == '}':
		result = encodeObj(value)
	elif value[0] == '[' and value[-1] == ']':
		result = encodeArr(value)
	elif value[0] == '"' and value[-1] == '"':
		result = encodeStr(value)
	elif value[0] == '-' or value[0].isdigit():
		result = eval(value)
		if result > sys.float_info.max or result < -sys.float_info.max:
			raise FormatError('Json format error: float overflow')
	elif value == 'true':
			result = True
	elif value == 'false':
		result = False
	elif value == 'null':
		result = None
	else:
		raise FormatError('Json format error: value format error')
	return result

def encodeObj(s):
	"""
	encode object
	"""
	d = {}
	s = s[1:]
	for item in mysplit(s, True):
		mid = objSplit(item)
		if mid == -1:
			raise FormatError('Json format error: object format error')
		key = item[:mid].strip()
		value = item[mid+1:]
		key = encodeStr(key)
		d[key] = encodeVal(value)
	return d

def encodeArr(s):
	"""
	encode array
	"""
	arr = []
	s = s[1:]
	for item in mysplit(s, False):
		arr.append(encodeVal(item))
	return arr

def encodeStr(s):
	"""
	encode string
	"""
	if not (s[0] == '"' and s[-1] == '"'):
		raise FormatError('Json format error: string format error')
	s = s[1:len(s)-1]
	result = []
	p = 0
	while p != len(s):
		if s[p] != '\\':
			result.append(s[p].decode('utf-8'))
			p += 1
		else:
			p += 1
			if BACKSLASH.has_key(s[p]):
				result.append(BACKSLASH[s[p]].decode('utf-8'))
				p += 1
			elif s[p] == 'u':
				esc = s[p+1:p+5]
				uni = int(esc, 16)
				result.append(unichr(uni))
				p += 5
	return ''.join(result)


def mysplit(s, isobj):
	"""
	split object or array
	"""
	item = ''
	while s:
		if isobj:
			p = objSplit(s)
			item += s[:p+1]
			s = s[p+1:]
		s = s.lstrip()
		if s[0] == '{':
			p = myfind(s, '{', '}')
			item += s[:p+1]
			s = s[p+1:]
			left = s.find(',') 
			if left == -1:
				s = ''
			else:
				s = s[left+1:]
		elif s[0] == '[':
			p = myfind(s, '[', ']')
			item += s[:p+1]
			s = s[p+1:]
			left = s.find(',') 
			if left == -1:
				s = ''
			else:
				s = s[left+1:]
		elif s[0] == '"':
			p = 1
			while s[p] != '"':
				if s[p] == '\\':
					p += 2
				else:
					p += 1
			item += s[:p+1]
			s = s[p+1:]
			left = s.find(',')
			if left != -1:
				item += s[:left]
				s = s[left+1:]
			else:
				item += s[:-1]
				s = ''
		else:
			left = s.find(',')
			if left != -1:
				item += s[:left]
				s = s[left+1:]
			else:
				item += s[:-1]
				s = ''
		if item.strip():
			yield item
		item = ''

def objSplit(s):
	"""
	split each item in object
	"""
	if s.find(':') == -1:
		return -1
	p = s.find('"') + 1 
	while s[p] != '"':
		if s[p] == '\\':
			p += 2
		else:
			p += 1
	result = p
	s = s[p+1:]
	p = s.find(':')
	result += p + 1
	return result

def myfind(s, tar1, tar2):
	"""
	find matched '{}' or '[]'
	"""
	count = 1
	p = 1 
	while p != len(s) and count != 0:
		if s[p] == '"':
			p += 1
			while s[p] != '"':
				if s[p] == '\\':
					p += 2
				else:
					p += 1
		elif s[p] == tar1:
			count += 1
		elif s[p] == tar2:
			count -= 1
		p += 1
	if p == len(s) and count != 0:
		raise FormatError('Json format error: not enough %s%s' % (tar1, tar2))
	return p-1

def decodeVal(value):
	"""
	decode each value
	"""
	if isinstance(value, dict):
		result = decodeObj(value)
	elif isinstance(value, list):
		result = decodeArr(value)
	elif isinstance(value, unicode):
		result = decodeStr(value)
	elif isinstance(value, bool):
		if value == True:
			result = 'true'
		else:
			result = 'false'
	elif value == None:
		result = 'null'
	elif isinstance(value, int) or isinstance(value, float):
		if value > sys.float_info.max or value < -sys.float_info.max:
			result = 'null'
		else:
			result = str(value)
	else:
		raise FormatError('Dict format error')
	return result

def decodeObj(d):
	"""
	decode object
	"""
	if not d:
		return '{}'
	json = '{'
	for key in d:
		json += decodeStr(key)
		json += ': '
		json += decodeVal(d[key])
		json += ', '
	json = json[:-2]
	json += '}'
	return json

def decodeArr(l):
	"""
	decode array
	"""
	if not l:
		return '[]'
	json = '['
	for i in l:
		json += decodeVal(i)
		json += ', '
	json = json[:-2]
	json += ']'
	return json

def decodeStr(s):
	"""
	decode string
	"""
	json = '"'
	for i in s:
		if ESCAPE_DCT.has_key(i):
			json += ESCAPE_DCT[i]
		elif ord(i) >= 0x21 and ord(i) <= 0x7e:
			json += i.encode('utf-8')
		elif ord(i) == 0x20:
			json += i.encode('utf-8')
		else:
			json += '\\u%04x' % ord(i)
	json += '"'
	return json

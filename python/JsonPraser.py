# coding = utf-8
"""
Implementation of JsonParser
"""
import sys, copy

ESCAPE_DCT = {
		'\\' : '\\\\',
		'"' : '\\"',
		'\b' : '\\b',
		'\f' : '\\f',
		'\n' : '\\n',
		'\r' : '\\r',
		'\t' : '\\t',
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

	def load(self, s):
		"""
		load string s in JSON format
		"""
		self.json = s
		self.jsonToDict(self.json)

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
		self.jsonToDict(self.json)

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

	def jsonToDict(self, s):
		"""
		transform json to dict
		"""
		s = s.strip()
		if s[0] == '{' and s[-1] == '}':
			self.d = conductObj(s)
		else:
			raise FormatError('Json format error: outermost layer must be object')

	def dictToJson():
		"""
		transform dict to json
		"""

def conductVal(value):
	"""
	conduct each value
	"""
	value = value.strip()
	if value[0] == '{' and value[-1] == '}':
		result = conductObj(value)
	elif value[0] == '[' and value[-1] == ']':
		result = conductArr(value)
	elif value[0] == '"' and value[-1] == '"':
		result = conductStr(value)
	elif value[0] == '-' or value[0].isdigit():
		result = eval(value)
		if result > sys.float_info.max or result < sys.float_info.min:
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

def conductObj(s):
	"""
	conduct object
	"""
	d = {}
	s = s[1:]
	for item in mysplit(s, True):
		mid = objSplit(item)
		if mid == -1:
			raise FormatError('Json format error: object format error')
		key = item[:mid].strip()
		value = item[mid+1:]
		key = conductStr(key)
		d[key] = conductVal(value)
	return d

def conductArr(s):
	"""
	conduct array
	"""
	arr = []
	s = s[1:]
	for item in mysplit(s, False):
		arr.append(conductVal(item))
	return arr

def conductStr(s):
	"""
	conduct string
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
			#if p == -1:
				#raise FormatError('Json format error: object format error')
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
	if s.find(':') == -1:
		return -1
	p = s.find('"') + 1 
	while not (s[p] == '"' and s[p-1] != '\\'):
		p += 1
	result = p
	s = s[p+1:]
	p = s.find(':')
	result += p + 1
	return result


def myfind(s, tar1, tar2):
	count = 1
	p = 1 
	while p != len(s) and count != 0:
		if s[p] == '"':
			p += 1
			while not (s[p] == '"' and s[p-1] != '\\'):
				p += 1
		elif s[p] == tar1:
			count += 1
		elif s[p] == tar2:
			count -= 1
		p += 1
	if p == len(s) and count != 0:
		raise FormatError('Json format error: not enough %s%s' % (tar1, tar2))
	return p-1




if __name__ == '__main__':
	a1 = JsonParser()
	test_json_str = '{ "\\tfm\\r": { "\\"fwl\\t": "\\/son\\u1234", "age\\b": 50 }, "\\ffwl": [ null, {}, [] ], "\\ncjp": null }'
	a1.load(test_json_str)
	a1.dumpJson('test')
	myd = a1.dumpDict()
	print 'myd1:', myd
	a2 = JsonParser()
	a2.loadJson('test')
	myd2 = a2.dumpDict()
	print 'myd2:', myd2

from JsonParser import JsonParser

def compared(d1, d2):
	for key in d1:
		if isinstance(d1[key], list):
			if not comparel(d1[key], d2[key]):
				print 'dict:%s not equal to %s' % (d1[key], d2[key])
				return False
		elif isinstance(d1[key], dict):
			if not compared(d1[key], d2[key]):
				print 'list:%s not equal to %s' % (d1[key], d2[key])
				return False
		else:
			if d1[key] != d2[key]:
				print 'element:%s not equal to %s' % (d1[key], d2[key])
				return False
	return True

def comparel(l1, l2):
	result = True
	for i in range(len(l1)):
		if isinstance(l1[i], list):
			if not comparel(l1[i], l2[i]):
				print 'dict:%s not equal to %s' % (l1[i], l2[i])
				return False
		elif isinstance(l1[i], dict):
			if not compared(l1[i], l2[i]):
				print 'list:%s not equal to %s' % (l1[i], l2[i])
				return False
		else:
			if l1[i] != l2[i]:
				print 'element:%s not equal to %s' % (l1[i], l2[i])
				return False
	return result

if __name__ == '__main__':
	a1 = JsonParser()
	a2 = JsonParser()
	a3 = JsonParser()
	a1.loadJson('./test')
	d1 = a1.dumpDict()
	print 'd1:', d1 
	a2.loadDict(d1)
	a2.dumpJson('./test1')
	a3.loadJson('./test1')
	d3 = a3.dumpDict()
	print 'd3:', d3
	if compared(d1, d3):
		print 'All is OK!'

	a1[u'root'][8][u'integer'] = 9876543210
	print a1[u'root'][8][u'integer']

	myd = {u'root':u'root', u'leaf':u'leaf'}
	a1.update(myd)

	print a1.dump()
	print a1.dumpDict()

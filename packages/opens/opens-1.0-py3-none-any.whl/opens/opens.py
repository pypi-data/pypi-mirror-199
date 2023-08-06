_ = {}

def r(response):
	print(f"\u001b[42m {response} \u001b[0m\u001b[32m\uE0B0\u001b[0m")

def put(variable, value):
	_[variable] = value
	return value

def get(variable):
	res = _[variable]
	r(res)
	return res

def echo(text, colour=1):
	print(f"\u001b[{colour}m{text}\u001b[0m")

def q(code=0):
	r(f"Exiting... code: {code}")
	quit(code)


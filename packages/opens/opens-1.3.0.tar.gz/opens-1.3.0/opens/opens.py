import os

_ = {}
cd = "/"

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

def prompt(text=None, colour=3):
	print(f"\u001b[44m  \u2753 {text} \u001b[0m\u001b[34m\uE0B0 ", end="")
	res = input(f"\u001b[0m\u001b[{colour}m")
	print("\u001b[0m", end="")
	return res

def fullpath(path):
	if path.startswith("/"):
		return path
	if os.path.exists(cd + "/" + path):
		return cd + "/" + path
	return "/"

def ls(path=""):
	p = fullpath(path)
	res = os.listdir(p)
	for i in res:
		print(i)
import os

_ = {}
cdir = "/"

def printc(text, bg):
	tsize = os.get_terminal_size()
	if tsize.columns > len(text) + 4:
		padding = " " * ((tsize.columns - len(text)) // 2 - 2)
		print(f"{padding}\u001b[0m\u001b[{bg-10}m\uE0B2\u001b[0m\u001b[{bg}m {text} \u001b[0m\u001b[{bg-10}m\uE0B0\u001b[0m")
	else:
		print(f"\u001b[0m\u001b[{bg-10}m{text}\u001b[0m")

def r(response):
	print(f"\u001b[42m {response} \u001b[0m\u001b[32m\uE0B0\u001b[0m")

def put(variable, value):
	_[variable] = value
	return value

def get(variable):
	res = _[variable]
	return res

def echo(text, colour=1):
	print(f"\u001b[{colour}m{text}\u001b[0m")

def q(code=0):
	quit(code)

def prompt(text=None, colour=3):
	print(f"\u001b[44m  \u2753 {text} \u001b[0m\u001b[34m\uE0B0 ", end="")
	res = input(f"\u001b[0m\u001b[{colour}m")
	print("\u001b[0m", end="")
	return res

def fullpath(path):
	if path.startswith("/"):
		return path
	if os.path.exists(cdir + "/" + path):
		return cdir + "/" + path
	return 

def ls(path=""):
	p = fullpath(path)
	if p:
		res = os.listdir(p)
		for i in res:
			print(i)
	else:
		print

def cd(path="-1"):
	global cdir
	p = fullpath(path)
	if path == "-1":
		return cdir
	if p:
		cdir = p
		return cdir
	printc("Invalid path!", 41)
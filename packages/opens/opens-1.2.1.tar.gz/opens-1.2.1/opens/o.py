import os
import opens

VERSION = "1.2"

def printc(text, bg):
	tsize = os.get_terminal_size()
	if tsize.columns > len(text) + 4:
		padding = " " * ((tsize.columns - len(text)) // 2 - 2)
		print(f"{padding}\u001b[0m\u001b[{bg-10}m\uE0B2\u001b[0m\u001b[{bg}m {text} \u001b[0m\u001b[{bg-10}m\uE0B0\u001b[0m")
	else:
		print(f"\u001b[0m\u001b[{bg-10}m{text}\u001b[0m")

def main():
	opens.cd = os.path.expanduser("~")
	print()
	printc(f"Welcome to OpenShell {VERSION}", 44)
	print()
	globs = {}
	for i in dir(opens):
		globs[i] = eval("opens." + i)
	banned_modules = ["__builtins__", "os"]
	for mod in banned_modules:
		globs[mod] = None
	while True:
		cmd = input(f"\u001b[0m\u001b[45m \uF07C {opens.cd} \u001b[0m\u001b[35m\uE0B0\u001b[0m \u001b[1m")

		#if cmd.strip().endswith(":"):
		#	x = None
		#	while x != "":
		#		x = input(f"\u001b[0m\u001b[45m   {(len(cd) + 4) * ' '} \u001b[0m\u001b[35m\uE0B0\u001b[0m ")
		#		cmd += f"\n    {x}"
		try:
			exec(cmd, globs)
		except TypeError as e:
			printc(f"The command '{cmd}' is not valid", 41)
		except Exception as e:
			printc(str(e), 41)


if __name__ == "__main__":
	main()

import os
import opens

VERSION = "0.1.dev1"

def printc(text, bg):
	tsize = os.get_terminal_size()
	if tsize.columns > len(text) + 4:
		padding = " " * ((tsize.columns - len(text)) // 2 - 2)
		print(f"{padding}\u001b[0m\u001b[{bg-10}m\uE0B2\u001b[0m\u001b[{bg}m {text} \u001b[0m\u001b[{bg-10}m\uE0B0\u001b[0m")
	else:
		print(f"\u001b[0m\u001b[{bg-10}m{text}\u001b[0m")

def main():
	cd = os.path.expanduser("~")
	print()
	printc(f"Welcome to OpenShell {VERSION}", 44)
	print()
	while True:
		cmd = input(f"\u001b[0m\u001b[45m \uF07C {cd} \u001b[0m\u001b[35m\uE0B0\u001b[0m ")
		globs = {}
		for i in dir(opens):
			globs[i] = eval("opens." + i)
		globs["__builtins__"] = None

		#if cmd.strip().endswith(":"):
		#	x = None
		#	while x != "":
		#		x = input(f"\u001b[0m\u001b[45m   {(len(cd) + 4) * ' '} \u001b[0m\u001b[35m\uE0B0\u001b[0m ")
		#		cmd += f"\n    {x}"
		try:
			exec(cmd, globs)
		except KeyError as e:
			printc(str(e), 41)
		except TypeError as e:
			printc(f"The command '{cmd}' is not valid", 41)
		except Exception as e:
			printc(str(e), 41)


if __name__ == "__main__":
	main()

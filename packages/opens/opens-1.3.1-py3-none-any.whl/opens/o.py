import os
import opens

VERSION = "1.3"

def main():
	opens.cdir = os.path.expanduser("~")
	print()
	opens.printc(f"Welcome to OpenShell {VERSION}", 44)
	print()
	globs = {}
	for i in dir(opens):
		globs[i] = eval("opens." + i)
	banned_modules = ["__builtins__", "os"]
	for mod in banned_modules:
		globs[mod] = None
	while True:
		cmd = input(f"\u001b[0m\u001b[45m \uF07C {opens.cdir} \u001b[0m\u001b[35m\uE0B0\u001b[0m \u001b[1m")

		#if cmd.strip().endswith(":"):
		#	x = None
		#	while x != "":
		#		x = input(f"\u001b[0m\u001b[45m   {(len(opens.cdir) + 4) * ' '} \u001b[0m\u001b[35m\uE0B0\u001b[0m ")
		#		cmd += f"\n    {x}"
		try:
			if len(cmd.splitlines()) == 1:
				res = eval(cmd, globs)
				if res:
					opens.r(res)
			else:
				exec(cmd, globs)
		except TypeError as e:
			opens.printc(f"The command '{cmd}' is not valid", 41)
		except Exception as e:
			opens.printc(str(e), 41)


if __name__ == "__main__":
	main()

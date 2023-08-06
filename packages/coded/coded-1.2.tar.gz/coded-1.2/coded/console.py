def write(*text, seperator="", end="", flush=True):
	print(seperator.join(text), end=end, flush=flush)
def writeline(*text, seperator="", flush=True):
	print(seperator.join(text), end="\n", flush=flush)

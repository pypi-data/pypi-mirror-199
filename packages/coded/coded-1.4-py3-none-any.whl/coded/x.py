import os

def write(*text, seperator="", end="", flush=True):
	text = list(text)
	for a in range(len(text)):
		text[a] = str(text[a])
	print(seperator.join(text), end=end, sep=seperator, flush=flush)

def writeline(*text, seperator="", flush=True):
	write(*text, seperator=seperator, end="\n", flush=flush)

def prompt(input_type):
	return input_type(input())

def clear():
	if os.name == "nt":
		os.system("cls")
	else:
		os.system("clear")

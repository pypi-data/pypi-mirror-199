import os
import random

def write(*text, seperator="", end="", flush=True):
	"""Prints the given text to the console"""
	text = list(text)
	for a in range(len(text)):
		text[a] = str(text[a])
	print(seperator.join(text), end=end, sep=seperator, flush=flush)

def writeline(*text, seperator="", flush=True):
	"""Prints the given text to the console, appends a \\n character"""
	write(*text, seperator=seperator, end="\n", flush=flush)

def prompt(input_type):
	"""Prompts the user for console input, then casts to input_type"""
	try:
		return input_type(input())
	except Exception as e:
		return e

def clear():
	"""Clear the console window"""
	if os.name == "nt":
		os.system("cls")
	else:
		os.system("clear")

def rand(minimum, maximum=None):
	"""Generate a random number between minimum (inclusive) and maximum (exclusive)"""
	if maximum == None:
		return random.randrange(minimum)
	return random.randrange(minimum, maximum)

def readf(path):
	with open(path) as f:
		return f.read()


import os, sys, random
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

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
	"""Read the given file"""
	with open(path) as f:
		return f.read()

def writef(path, content):
	"""Write content to the given file"""
	with open(path, "w") as f:
		return f.write(content)

def rm(path):
	"""Remove a given file"""
	os.remove(path)

def rmdir(path):
	"""Remove a given directory, assuming it is empty"""
	os.rmdir(path)

def syscmd(cmd):
	"""Run a system (terminal) command"""
	os.system(cmd)

envs = os.environ 
"""Environment variables for your program"""

pypath = sys.path
"""Python path - contains the path of libraries"""

class Window:
	"""The Window class allows you to create GUI apps or games using Python!
	Based on the pygame library"""
	def __init__(self, width=640, height=480, title="Coded application"):
		pygame.init()
		self.window = pygame.display.set_mode((width, height))
		pygame.display.set_caption(title)

	def run(self):
		self.running = True
		
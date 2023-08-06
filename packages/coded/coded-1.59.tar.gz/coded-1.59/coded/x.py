import os, sys, random, enum
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

class Colour():
	RED = (255, 0, 0)
	GREEN = (0, 255, 0)
	BLUE = (0, 0, 255)
	YELLOW = (255, 255, 0)
	CYAN = (0, 255, 255)
	MAGENTA = (255, 0, 255)

class Ansi():
	RESET = "\u001b[0m"
	FBLACK = "\u001b[30m"
	BBLACK = "\u001b[40m"
	FRED = "\u001b[31m"
	BRED = "\u001b[41m"
	FGREEN = "\u001b[32m"
	BGREEN = "\u001b[42m"
	FBLUE = "\u001b[34m"
	BBLUE = "\u001b[44m"
	FYELLOW = "\u001b[33m"
	BYELLOW = "\u001b[43m"	
	FCYAN = "\u001b[36m"
	BCYAN = "\u001b[46m"
	FMAGENTA = "\u001b[35m"
	BMAGENTA = "\u001b[45m"
	FWHITE = "\u001b[37m"
	BWHITE = "\u001b[47sm"

	FLBLACK = "\u001b[30;1m"
	BLBLACK = "\u001b[40;1m"
	FLRED = "\u001b[31;1m"
	BLRED = "\u001b[41;1m"
	FLGREEN = "\u001b[32;1m"
	BLGREEN = "\u001b[42;1m"
	FLBLUE = "\u001b[34;1m"
	BLBLUE = "\u001b[44;1m"
	FLYELLOW = "\u001b[33;1m"
	BLYELLOW = "\u001b[43;1m"	
	FLCYAN = "\u001b[36;1m"
	BLCYAN = "\u001b[46;1m"


class Window:
	"""The Window class allows you to create GUI apps or games using Python!
	Based on the pygame library"""
	def __init__(self, width=640, height=480, title="Coded application"):
		self.window = pygame.display.set_mode((width, height))
		pygame.display.set_caption(title)
		self.events = {
			pygame.QUIT: self.quit_window
		}

	def run(self):
		self.running = True
		while self.running:
			for event in pygame.event.get():
				if event.type in self.events:
					self.events[event.type](event)
			pygame.display.flip()
			pygame.display.update()
		pygame.quit()
	
	def quit_window(self, event):
		self.running = False

	def event(self, event_type, callback):
		self.events[event_type] = callback

	def keydown(self, callback):
		self.event(pygame.KEYDOWN, callback)

	def keyup(self, callback):
		self.event(pygame.KEYUP, callback)

	def mousedown(self, callback):
		self.event(pygame.MOUSEBUTTONDOWN, callback)

	def mouseup(self, callback):
		self.event(pygame.MOUSEBUTTONUP, callback)

	def mousex(self):
		return pygame.mouse.get_pos()[0]

	def mousey(self):
		return pygame.mouse.get_pos()[1]

	def mousepos(self):
		return pygame.mouse.get_pos()

	def keys_pressed(self):
		return pygame.key.get_pressed()

	def key_is_down(self, key):
		return self.keys_pressed()[key]


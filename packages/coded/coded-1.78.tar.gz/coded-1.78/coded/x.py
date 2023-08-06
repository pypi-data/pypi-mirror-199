import os
import sys
import random
import enum
import time
import requests
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

	def __init__(self, colour):
		if type(colour) == str:
			self.hexa = colour
			self.red, self.green, self.blue = Colour.hex_to_rgb(self.hexa)
		if type(colour) == tuple:
			self.red, self.green, self.blue = colour
			self.hexa = Colour.rgb_to_hex(colour)

	def hex_to_rgb(hexa):
		hex_to_dec = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "a": 10, "b": 11, "c": 12, "d": 13, "e": 14, "f": 15}
		red = hex_to_dec[hexa[1]] * 16 + hex_to_dec[hexa[2]]
		green = hex_to_dec[hexa[3]] * 16 + hex_to_dec[hexa[4]]
		blue = hex_to_dec[hexa[5]] * 16 + hex_to_dec[hexa[6]]
		return (red, green, blue)

	def rgb_to_hex(rgb):
		dec_to_hex = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
		red_hex = dec_to_hex[rgb[0] // 16] + dec_to_hex[rgb[0] % 16]
		green_hex = dec_to_hex[rgb[1] // 16] + dec_to_hex[rgb[1] % 16]
		blue_hex = dec_to_hex[rgb[2] // 16] + dec_to_hex[rgb[2] % 16]
		return f"#{red_hex}{green_hex}{blue_hex}"

	def __str__(self):
		return self.hexa

	def __eq__(self, other):
		if type(other) == Colour:
			return self.hexa == other.hexa
		if type(other) == str:
			return self.hexa == other
		if type(other) == tuple:
			return self.red == other[0] and self.green == other[1] and self.blue == other[2]
		return False

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
	FLMAGENTA = "\u001b[35;1m"
	BLMAGENTA = "\u001b[45;1m"
	FLWHITE = "\u001b[37;1m"
	BLWHITE = "\u001b[47s;1m"


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

class Time:
	def __init__(self, time=time.time()):
		self.time = time
		self.convert_time
	
	def convert_time(self):
		self.second = time.localtime(self.time).tm_sec
		self.minute = time.localtime(self.time).tm_min
		self.hour = time.localtime(self.time).tm_hour
		self.mday = time.localtime(self.time).tm_mday
		self.wday = time.localtime(self.time).tm_wday
		self.yday = time.localtime(self.time).tm_yday
		self.month = time.localtime(self.time).tm_mon
		self.wday = time.localtime(self.time).tm_year

def delay(seconds):
	time.sleep(seconds)

def request_get(url):
	return requests.get(url)

def request_get_content(url):
	return requests.get(url).content

def request_get_cookies(url):
	return requests.get(url).cookies

def request_post(url, json):
	return requests.post(url, json=json)

def request_post_content(url, json):
	return requests.post(url, json=json).content


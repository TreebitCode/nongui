from os import system as batch
from time import sleep
from io_control import *
from display import *
from style import *

# ADD
# block alignment
# text alignment within block

# FIX
# improve text display speed

# === CLASSES =====  

# block of text with position and styling
class Block:

	def __init__(self, pos=(1, 1), content='', style=''):
		self.x = pos[0]  # horizontal coordinate
		self.y = pos[1]  # vertical coordinate
		self.content = content  # contained text
		self.style = style  # styling

	# move block relative to current position
	def move(self, x=1, y=0):
		self.x += int(x)
		self.y += int(y)

	# set block postition to specified coordinates
	def jump(self, x=1, y=1):
		if x: self.x = int(x)
		if y: self.x = int(y)

	# return text with applied styling
	def get(self): return f'{self.style}{self.content}{un()}'

	# display text with styling at position
	def draw(self):
		jump(self.x, self.y)
		disp(self.get())

	# erase all contained text
	def clear(self):
		jump(self.x, self.y)
		disp(''.join([c if ord(c) < 32 or c == '\x7f' else ' ' for c in self.get()]))

# rectangular text container with fixed dimensions
class Window(Block):

	def __init__(self, size, pos=[1, 1], content='', style=''):
		self.x = pos[0]  # horizontal coordinate
		self.y = pos[1]  # vertical coordinate
		self.w = size[0]  # width
		self.h = size[1]  # height
		self.content = content  # contained text
		self.style = style  # styling

	# return text with applied size limitations and styling
	def get(self):
		# accounting for width 
		render, counter = '', 0
		width = min(self.w, getw())
		for c in self.content:
			render, counter = render + c, counter + 1
			if counter == width: render, counter = render + '\n', 0
		# accounting for height
		overflow = (render.count('\n') + 1) - self.h
		while overflow > 0: render, overflow = render[render.find('\n')+1:], overflow-1
		# applying styling
		return f'{self.style}{render}{un()}'

# rectangular fixed dimensions container for keyboard input
class InputWindow(Window):

	def __init__(self, size, pos=[1, 1], content='', style=''):
		self.x = pos[0]  # horizontal coordinate
		self.y = pos[1]  # vertical coordinate
		self.w = size[0]  # width
		self.h = size[1]  # height
		self.content = content.split('\n')  # contained text
		self.style = style  # styling
		self.curs = Cursor(self)  # cursor

	# wait for and process keypress
	def key(self):
		c = unnp(key())
		y = self.curs.y
		if len(c) == 1: self.add(c)
		elif c == 'ENTER': self.newline()
		elif c == 'BACKSPACE':
			if self.curs.x: self.erase()
			elif self.curs.y: self.merge_up()
		elif c == 'LEFT':
			if self.curs.x: self.curs.left()
			elif self.curs.y: self.curs.jump(len(self.content[y-1]), y-1)
		elif c == 'RIGHT':
			if self.curs.x != len(self.content[y]): self.curs.right()
			elif self.curs.y != len(self.content) - 1: self.curs.jump(0, y+1)
		elif c == 'UP':
			if self.curs.y: self.curs.jump(min(self.curs.pref, len(self.content[self.curs.y-1])), y-1)
			else:
				self.curs.jump(0)
				self.curs.pref = 0
		elif c == 'DOWN':
			if self.curs.y != len(self.content)-1: self.curs.jump(min(self.curs.pref, len(self.content[self.curs.y+1])), self.curs.y+1)
			else:
				self.curs.jump(len(self.content[y]), -1)
				self.curs.pref = self.curs.x
		elif c == 'TAB': self.add(' ' * 4)
		elif c == 'DELETE':
			if self.curs.x == len(self.content[y]) and y != len(self.content)-1: self.merge_down()
			else: self.delete()
		elif c == 'HOME': self.curs.jump(0, -1)
		elif c == 'END': self.curs.jump(len(self.content[y]), -1)
		if c not in ('UP', 'DOWN'): self.curs.pref = self.curs.x
		return c

	# add character to contained text
	def add(self, chars):
		y = self.curs.y
		# add characters to line
		self.content[y] = f'{self.content[y][:self.curs.x]}{chars}{self.content[y][self.curs.x:]}'
		# display added characters and those after them
		disp(self.content[y][self.curs.x:])
		# return to cursor position before added characters
		left(len(self.content[y][self.curs.x:]))
		# move to position after added characters
		self.curs.right(len(chars))

	# add new line
	def newline(self):
		self.content.insert(self.curs.y+1,self.content[self.curs.y][self.curs.x:])
		self.content[self.curs.y] = self.content[self.curs.y][:self.curs.x]
		disp(' '*len(self.content[self.curs.y+1]))
		pos = (0, self.curs.y+1)
		line = self.curs.y + 1
		last_line = len(self.content)-1
		while line != last_line:
			self.curs.jump(0,self.curs.y+1)
			disp(self.content[line].ljust(len(self.content[line+1]),' '))
			line += 1
		self.curs.jump(0,self.curs.y+1)
		disp(self.content[line])
		self.curs.jump(*pos)

	# join current and previous line
	def merge_up(self):
		curr = self.content[self.curs.y]
		prev = self.content[self.curs.y - 1]
		self.content[self.curs.y] = ''.join(self.content[self.curs.y-1:self.curs.y+1])
		self.content.pop(self.curs.y-1)
		self.curs.jump(len(prev), self.curs.y-1)
		pos = (self.curs.x, self.curs.y)
		disp(curr)
		for line in range(self.curs.y+1, len(self.content)):
			self.curs.jump(0, self.curs.y+1)
			disp(self.content[line].ljust(len(self.content[line-1]),' '))
		self.curs.jump(0, self.curs.y+1)
		disp(' '*len(self.content[-1]))
		self.curs.jump(*pos)

	# join current and following line
	def merge_down(self):
		self.curs.jump(0, self.curs.y+1)
		self.merge_up()

	# remove character before cursor
	def erase(self):
		y = self.curs.y
		# erase character from line
		self.content[y] = f'{self.content[y][:self.curs.x-1]}{self.content[y][self.curs.x:]}'
		# move cursor over character that is being erased
		self.curs.left()
		# display characters after character that is being erased
		disp(self.content[y][self.curs.x:]+' ')
		# return to cursor position of erased character
		left(len(self.content[y][self.curs.x:])+1)

	# delete character after/under cursor
	def delete(self):
		y = self.curs.y
		# delete character from line
		self.content[y] = f'{self.content[y][:self.curs.x]}{self.content[y][self.curs.x+1:]}'
		# display characters after character that is being deleted
		disp(self.content[y][self.curs.x:]+' ')
		# return to initial cursor position
		left(len(self.content[y][self.curs.x:])+1)

	# display text
	def draw(self):
		self.curs.jump(0, 0)
		disp(f'{self.style}{self.content[0]}')
		for line in self.content[1:]:
			self.curs.jump(0, self.curs.y + 1)
			disp(line)
		self.curs.jump(len(self.content[self.curs.y]))
		self.curs.pref = self.curs.x
		disp(un())

# input window cursor 
class Cursor:

	def __init__(self, window):
		self.x, self.y = 0, 0  # relative coordinates
		self.window = window  # parent input text window
		self.pref = self.x  # preferred cursor position when moving to different line

	# move relative to current position
	def move(self, x=1, y=0):
		self.x += x
		self.y += y
		move(x, y)

	# move in specified direction
	def left(self, s=1):  self.move(-s)
	def right(self, s=1):  self.move(s)
	def up(self, s=1):  self.move(0,-s)
	def down(self, s=1): self.move(0,s)

	# jump to specified coordinates
	def jump(self, x=-1, y=-1):
		if x >= 0: self.x = x
		if y >= 0: self.y = y
		jump(self.window.x + self.x, self.window.y + self.y)

# === OTHER =====

# initialize escape sequence recognition and set up display
def init(clear_screen=True, home=True, show_cursor=True):
	batch('')
	if clear_screen: clear(home)
	cursor(show_cursor)

# fps control
def fps(frames): sleep(1/frames)
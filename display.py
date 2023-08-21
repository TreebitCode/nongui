from os import system as batch
from os import get_terminal_size
from msvcrt import kbhit as keyboard
from msvcrt import putwch, getwch, ungetwch

# === ESCAPE SEQUENCES =====

# generate ANSI escape sequence and run it
def esc(code, p='['):
	for char in f'\x1b{p}{code}': putwch(char)

# === DISPLAY =====

# clear screen
def clear(home=False):
	if not home: pos = getxy()  # save position
	batch('CLS')
	if not home: jump(*pos)  # return to position

# get terminal window resolution in chars
def getwh(): return get_terminal_size()[:]
def getw(): return get_terminal_size()[0]  # width only
def geth(): return get_terminal_size()[1]  # height only

# set terminal window title
def title(string): batch(f'TITLE {string}')

# === CURSOR =====

# get cursor position coordinates
def getxy():
	# saving unprocessed keypresses
	# to separate requested data
	unprocessed = ''
	while keyboard():
		key = getwch()
		unprocessed += key
		if key in '\0à': unprocessed += getwch()
	# request coordinates using escape sequence
	esc('6n')
	# read returned data from standard input
	data = ''
	while keyboard(): data += getwch()
	# reestablish unprocessed keypresses
	for key in unprocessed: ungetwch(key)
	# return x and y as tuple
	sc = data.find(';')
	return (int(data[sc+1:-1]), int(data[2:sc]))

def getx(): getxy()[0]  # x only
def gety(): getxy()[1]  # y only

# move cursor relative to current position
def move(x=1, y=0):
	if x < 0: esc(f'{-x}D')
	elif x:  esc(f'{x}C')
	if y < 0: esc(f'{-y}A')
	elif y: esc(f'{x}B')

# move cursor in specified direction
def left(s):  move(-s)
def right(s):  move(s)
def up(s):  move(0,-s)
def down(s): move(0,s)

# set cursor postition to specified coordinates
def jump(x=1, y=1):
	if not x: esc(f'{y}d')
	elif not y: esc(f'{x}G')
	else: esc(f'{y};{x}H')

# set cursor position to top left corner
def home(): jump(1, 1)
# set cursor position to bottom left corner
def end(): jump(0, geth())

# control visibility, shape and blinking of cursor
def cursor(show=True, blink=True):
	# block, underline, bar, thick underline
	shapes = {'#': 2, '_': 4, '|': 6, '=': 7}
	# set shape
	if str(show) in '#_|=':
		shape = shapes[show]
		if blink: shape -= 1
		esc(f'{shape} q')
		if shape == 7: blink()
	# set visibility and blinking
	show_cursor(show)
	blink_cursor(blink)

# control cursor visibility
def show_cursor(s=True):
	if s: esc('?12h')
	else: esc('?12l')

# control cursor blinking
def blink_cursor(b=True):
	if b: esc('?25h')
	else: esc('?25l')
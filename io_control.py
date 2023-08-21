from msvcrt import kbhit as keyboard
from msvcrt import putwch, getwch

# === DISPLAYING TEXT =====

# display exact string on screen
def disp(string):
	for char in string: putwch(char)

# disp() without changing cursor position
def edit(string):
	# save cursor position
	for c in '\x1b[6n': putwch(c)
	rep = ''
	while keyboard(): rep += getwch()
	sem = rep.find(';')
	x, y = int(rep[sem+1:-1]), int(rep[2:sem])
	# display string
	for c in string: putwch(c)
	# return to saved position
	for c in f'\x1b[{y};{x}H': putwch(c)

# display data on screen as text
def text(*data, sep=' ', end=''):
	data = f'{str(sep).join([str(d) for d in data])}{end}'
	for char in data: putwch(char)

# === ESCAPE SEQUENCES =====

# generate escape sequence and run it
def esc(code, p='['):
	sequence = f'\x1b{p}{code}'
	for char in data: putwch(char)

# generate escape sequence without running it
def seq(code, p='['): return f'\x1b{p}{code}'

# === KEYBOARD INPUT =====

# read characters from keyboard input
def getch(hits=1):
	chars = ''
	for hit in range(hits): chars += getwch()
	while not hits and keyboard(): chars += getwch()
	return chars

# read key presses from keyboard input
def key(hits=1):
	keys = []
	for hit in range(hits):
		kp = getwch()
		# two byte keypresses
		if kp in '\0à': kp += getwch()
		# convert non-character key to readable name
		# and add it to list
		keys.append(convert_key(kp))
	if len(keys) == 1: return keys[0]
	return keys

def convert_key(kp):
	# readable names for special keys and shortcuts
	onebyte = {
		'\x01': 'CTRL+A', '\x02': 'CTRL+B', '\x03': 'CTRL+C',
		'\x04': 'CTRL+D', '\x05': 'CTRL+E',	'\x06': 'CTRL+F',
		'\x07': 'CTRL+G', '\b': 'BACKSPACE', '\t': 'TAB',
		'\n': 'CTRL+J', '\v': 'CTRL+K', '\f': 'CTRL+L',
		'\r': 'ENTER', '\x0e': 'CTRL+N', '\x0f': 'CTRL+O',
		'\x10': 'CTRL+P', '\x11': 'CTRL+Q', '\x12': 'CTRL+R',
		'\x13': 'CTRL+S', '\x14': 'CTRL+T', '\x15': 'CTRL+U',
		'\x16': 'CTRL+V', '\x17': 'CTRL+W', '\x18': 'CTRL+X',
		'\x19': 'CTRL+Y', '\x1a': 'CTRL+Z', '\x1b': 'ESC',
		'\x1c': 'CTRL+\\', '\x1d': 'CTRL+]', '\x1e': 'CTRL+^',
		'\x1f': 'CTRL+_', '\x7f': 'CTRL+BACKSPACE'}
	twobyte = {
		'\0\x03': 'CTRL+2', '\0\x0e': 'ALT+CTRL+BACKSPACE',
		'\0\x10': 'ALT+CTRL+Q', '\0\x11': 'ALT+CTRL+W',
		'\0\x12': 'ALT+CTRL+E', '\0\x13': 'ALT+CTRL+R',
		'\0\x14': 'ALT+CTRL+T', '\0\x15': 'ALT+CTRL+Y',
		'\0\x16': 'ALT+CTRL+U', '\0\x17': 'ALT+CTRL+I',
		'\0\x18': 'ALT+CTRL+O', '\0\x19': 'ALT+CTRL+P',
		'\0\x1a': 'ALT+CTRL+[', '\0\x1b': 'ALT+CTRL+]',
		'\0\x1c': 'ALT+CTRL+ENTER', '\0\x1e': 'ALT+CTRL+A',
		'\0\x1f': 'ALT+CTRL+S', '\0 ': 'ALT+CTRL+D',
		'\0!': 'ALT+CTRL+F', '\0"': 'ALT+CTRL+G',
		'\0#': 'ALT+CTRL+H', '\0$': 'ALT+CTRL+J',
		'\0%': 'ALT+CTRL+K', '\0&': 'ALT+CTRL+L',
		'\0\'': 'ALT+CTRL+;', '\0(': 'ALT+CTRL+\'',
		'\0)': 'ALT+CTRL+`', '\0,': 'ALT+CTRL+Z',
		'\0-': 'ALT+CTRL+X', '\0.': 'ALT+CTRL+C',
		'\0/': 'ALT+CTRL+V', '\0\x30': 'ALT+CTRL+B',
		'\0\x31': 'ALT+CTRL+N', '\0\x32': 'ALT+CTRL+M',
		'\0\x33': 'ALT+CTRL+<', '\0\x34': 'ALT+CTRL+>',
		'\0\x35': 'ALT+CTRL+/', '\0;': 'F1', '\0<': 'F2',
		'\0=': 'F3', '\0>': 'F4', '\0?': 'F5', '\0@': 'F6',
		'\0A': 'F7', '\0B': 'F8', '\0C': 'F9', '\0D': 'F10',
		'\0G': 'HOME', '\0H': 'UP NP', '\0I': 'PAGE UP',
		'\0K': 'LEFT NP', '\0M': 'RIGHT NP', '\0O': 'END',
		'\0P': 'DOWN NP', '\0Q': 'PAGE DOWN',
		'\0R': 'INSERT\x20NP', '\0S': 'DELETE\x20NP',
		'\0^': 'CTRL+F1', '\0_': 'CTRL+F2',	'\0`': 'CTRL+F3',
		'\0a': 'CTRL+F4', '\0b': 'CTRL+F5', '\0c': 'CTRL+F6',
		'\0d': 'CTRL+F7', '\0e': 'CTRL+F8', '\0f': 'CTRL+F9',
		'\0g': 'CTRL+F10', '\0h': 'ALT+F1', '\0i': 'ALT+F2',
		'\0j': 'ALT+F3', '\0k': 'ALT+F4', '\0l': 'ALT+F5',
		'\0m': 'ALT+F6', '\0n': 'ALT+F7', '\0o': 'ALT+F8',
		'\0p': 'ALT+F9', '\0q': 'ALT+F10', 
		'\0s': 'CTRL+LEFT NP', '\0t': 'CTRL+RIGHT NP',
		'\0u': 'CTRL+END', '\0v': 'CTRL+PAGE DOWN',
		'\0w': 'CTRL+HOME', '\0x': 'ALT+CTRL+1',
		'\0y': 'ALT+CTRL+2', '\0z': 'ALT+CTRL+3',
		'\0{': 'ALT+CTRL+4', '\0|': 'ALT+CTRL+5',
		'\0}': 'ALT+CTRL+6', '\0~': 'ALT+CTRL+7',
		'\0\x7f': 'ALT+CTRL+8', '\0\x80': 'ALT+CTRL+9',
		'\0\x81': 'ALT+CTRL+0', '\0\x82': 'ALT+CTRL+-',
		'\0\x83': 'ALT+CTRL+=', '\0\x84': 'CTRL+PAGE UP',
		'\0\x8d': 'CTRL+UP NP', '\0\x91': 'CTRL+DOWN NP',
		'\0\x92': 'CTRL+INSERT NP', '\0\x93': 'CTRL+DELETE NP',
		'\0\x94': 'CTRL+TAB', '\0\x98': 'ALT+CTRL+UP',
		'\0\x9b': 'ALT+CTRL+LEFT', '\0\x9d': 'ALT+CTRL+RIGHT',
		'\0\xa0': 'ALT+CTRL+DOWN', '\0\xa4': 'ALT+CTRL+/ NP',
		'\0\xa6': 'ALT+CTRL+ENTER NP', 'àH': 'UP',
		'àK': 'LEFT', 'àM': 'RIGHT', 'àP': 'DOWN',
		'àR': 'INSERT', 'àS': 'DELETE', 'às': 'CTRL+LEFT',
		'àt': 'CTRL+RIGHT', 'à\x85': 'F11', 'à\x86': 'F12',
		'à\x89': 'CTRL+F11', 'à\x8a': 'CTRL+F12',
		'à\x8b': 'ALT+F11', 'à\x8c': 'ALT+F12',
		'à\x8d': 'CTRL+UP', 'à\x91': 'CTRL+DOWN',
		'à\x92': 'CTRL+INSERT',	'à\x93': 'CTRL+DELETE'}
	
	if kp in onebyte: return onebyte[kp]
	elif kp in twobyte: return twobyte[kp]
	return kp

# remove np from keypress text
def unnp(kp):
	if kp[-2:] == 'NP': return kp[:-3]
	return kp

# stop execution until any character is entered
def wait(): return getwch()

# stop execution until one of specified characters is entered
def wait_for(chars):
	char = getwch()
	while not char in chars: char = getwch()
	return char
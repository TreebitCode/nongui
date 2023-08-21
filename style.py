# === STYLING =====

# font styles (bold, underlined, inverted colors)
def bold(): return '\x1b[1m'
def under(): return '\x1b[4m'
def invert(): return '\x1b[7m'

# undo styles
def un(): return '\x1b[0m'  # clear all styling
def unbold(): return '\x1b[22m'
def ununder(): return '\x1b[24m'
def uninvert(): return '\x1b[27m'

# === COLORS =====

# convert hexadecimal number to decimal
def dec(string): return int(string, base=16)

# convert decimal number to tuple of RGB values
def rgb(integer):
	h = '{:06x}'.format(integer)
	return (dec(h[:2]), dec(h[2:4]), dec(h[4:]))

# colors
def color(fg='a', bg=-1):
	code = []
	if fg != -1:
		if type(fg) is str:
			if fg[0] == '#': fg = fg[1:]
			if len(fg) == 1: fg = color4(fg)
			elif len(fg) == 2: fg = color4(fg[1], fg[0])
			elif len(fg) == 3: fg = color24((dec(fg[0]*2), dec(fg[1]*2), dec(fg[2]*2)))
			else: fg = color24((dec(fg[:2]), dec(fg[2:4]), dec(fg[4:])))
		elif type(fg) is int and fg != -1:
			if fg < 16: fg = color4(fg)
			elif fg < 256: fg = color8(fg)
			else: fg = color24(rgb(fg))
		else: fg = color24(fg)
		code.append(fg)
	if bg != -1:
		if type(bg) is str:
			if bg[0] == '#': bg = bg[1:]
			if len(bg) == 1: bg = color4(-1, bg)
			elif len(bg) == 3: bg = color24(0, dec((bg[0]*2), dec(bg[1]*2), dec(bg[2]*2)))
			else: bg = color24(0, (dec(bg[:2]), dec(bg[2:4]), dec(bg[4:])))
		elif type(bg) is int and bg != -1:
			if bg < 16: bg = color4(-1, bg)
			elif bg < 256: bg = color8(-1, bg)
			else: bg = color24(0, rgb(bg))
		else: bg = color24(0, bg)
		code.append(bg)
	if len(code) == 2: code = [code[0] + code[1]]
	return code[0]

# reinterpret 4-bit color code according to default cmd color order
def cmd(code): return [0,4,2,6,1,5,3,7,8,12,10,14,9,13,11,15][int(code, base=16)]

# 4-bit colors
def color4(fg=-1, bg=-1):
	code = []
	fg, bg = cmd(fg), cmd(bg)
	if bg > 7: bg += 52
	if fg > 7: fg += 52
	if bg >= 0: code.append(bg + 40)
	if fg >= 0: code.append(fg + 30)
	code = [str(g) for g in code]
	return f'\x1b[{";".join(code)}m'

# 8-bit colors
def color8(fg=-1, bg=-1):
	code = []
	fg, bg = int(fg), int(bg)
	if bg >= 0: code.append(f'48;5;{bg}')
	if fg >= 0: code.append(f'38;5;{fg}')
	return f'\x1b[{";".join(code)}m'

# 24-bit colors
def color24(fg=(255, 0, 0), bg=()):
	code = []
	if bg: code.append(f'48;2;{";".join([str(int(c)) for c in bg])}')
	if fg: code.append(f'38;2;{";".join([str(int(c)) for c in fg])}')
	return f'\x1b[{";".join(code)}m'
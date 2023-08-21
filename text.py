from ngui import *

init()
title('Text editor')
field = InputWindow(getwh(), content='Monday\nTuesday\nWednesday\nThursday\nFriday\nSaturday\nSunday')
field.draw()
char = field.key()
while char != 'ESC': char = field.key()
clear(1)
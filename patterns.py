from math import pi

def constant(number, time, colour, freq):
	return colour
def flash(number, time, colour, freq):
	return colour if int(freq*time) % 2 else [0,0,0]
#!/usr/bin/env python
import patterns
import operator as op
from time import time, sleep
from math import sin, pi
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--colour", '-c', help ='integer 0-255 r,g,b', default="10,40,0")
parser.add_argument("--resolution", '-r', help ='updates per second',
                    default = 30.0, type=float)
parser.add_argument("--number", '-n', help='number of leds', default = 50, type=int)
parser.add_argument("--dryrun", help='do not try access the spi device (for testing)', action="store_true")
parser.add_argument("--pattern", '-p', help="select the pattern to be displayed", default = "constant")
parser.add_argument("--frequency", '-f', help="control the frequency of patterns (Hz)", type = float, default = 1.0)

args = parser.parse_args()

off = [0,0,0]
colour_map = {'orange': '80,40,0', 'red':'80,0,0', 'green':'10,40,0', 'blue':'0,0,80', 'white':'40,40,40'}

def cie1931(L):
    L = L*100.0/255.0
    if L <= 8:
        return (L/902.3)*255.0
    else:
        return ((L+16.0)/116.0)**3.0 *255.0

def print_function(s):
    print s

def set_led(colours):
    if args.dryrun:
        print "set leds to {}".format(colours)
    else:
        spi.write("".join(chr(int(i)) for colour in colours for i in colour))
        spi.flush()

def get_spi_device():
    if args.dryrun:
        return open("/dev/null", 'w')
    else:
        return open("/dev/spidev0.0", 'w')


with get_spi_device() as spi:
    colour = colour_map.get(args.colour, args.colour)
    rgb =[int(cie1931(float(c))) for c in colour.split(',')]
    col_func = op.attrgetter(args.pattern)
    col_func = col_func(patterns)
    while True:
        data = [col_func(n, time(), rgb, args.frequency) for n in range(args.number)]
        set_led(data)
        sleep(1.0/args.resolution)



    		

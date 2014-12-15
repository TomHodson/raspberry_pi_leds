#!/usr/bin/env python
from time import time, sleep
from math import sin, pi
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--colour", '-c', help ='integer 0-255 r,g,b', default="10,40,0")
parser.add_argument("--resolution", '-r', help ='updates per second',
                    default = 30.0, type=float)
parser.add_argument("--number", '-n', help='number of leds', default = 1, type=int)
parser.add_argument("--dryrun", help='do not try access the spi device (for testing)', action="store_true")

modes = parser.add_mutually_exclusive_group()
modes.add_argument("--flash", '-f', help ='square wave (Hz)',
                    type=float)
modes.add_argument("--pulse", '-p', help ='sine wave (Hz)',
                    type=float)
modes.add_argument("--phasor", help='moving wavefront', 
                    type=float)

args = parser.parse_args()

off = [0,0,0]
colours = {'orange': '80,40,0', 'red':'80,0,0', 'green':'10,40,0', 'blue':'0,0,80', 'white':'40,40,40'}

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
        spi.write("".join(chr(int(i)) for i in colour for colour in colours))
        spi.flush()

def get_spi_device():
    if args.dryrun:
        return open("/dev/null", 'w')
    else:
        return open("/dev/spidev0.0", 'w')


with get_spi_device() as spi:
#if True:
    colour = colours.get(args.colour, args.colour)
    colours = [[int(cie1931(float(c))) for c in colour.split(',')] for _ in range(args.number or 1)]
    set_led(colours)
    while args.flash:
        set_led(off)
        sleep(1.0/args.flash)
        set_led(colours)
        sleep(1.0/args.flash)
    while args.pulse:
        s = sin(2*pi*time()*args.pulse)
        s = (s+1.0)/2.0
        c = [[i*s for i in colour] for colour in colours]
        set_led(c)
        sleep(1.0/(args.resolution))


    		

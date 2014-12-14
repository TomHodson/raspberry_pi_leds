raspberry_pi_leds
=================

Some scripts to control spi based RGB LEDs on a Raspberry Pi

Should work with any spi based LEDs connected to /dev/spidev0.0

led.py
-------
options
- specifiy colours by component or name ie "--colour 20,40,0" or "--colour red"
- flash led at 2 Hz "--flash 2"
- pulse (sine wave) "--pulse 2"
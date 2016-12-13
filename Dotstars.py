#!/usr/bin/python

# Light-painting example for Adafruit Dot Star RGB LED strip.
# Loads image, displays column-at-a-time on LEDs at a reasonable speed
# for long exposure photography.
# See strandtest.py for a much simpler example script.
# See image-pov.py for a faster persistence-of-vision example.

#from PIL import Image
#from dotstar import Adafruit_DotStar

##
## Python module to control for APA102C ledstripes (Adafruit Dotstars) on the Wipy 
##   
##

from pyb import SPI

class DotStars:
    "Doc String for this class"    
    
    def __init__(self, leds):
        self.ledcount = leds
        self.buffersize = self.ledcount * 4
        self.buffer = bytearray(self.ledcount * 4)
        self.emptybuffer = bytearray(self.ledcount * 4)
        for i in range(0, self.buffersize, 4):
            self.emptybuffer[i] = 0xff
            self.emptybuffer[i + 1] = 0x0
            self.emptybuffer[i + 2] = 0x0
            self.emptybuffer[i + 3] = 0x0   
        self.startframe = bytes([0x00, 0x00, 0x00, 0x00])
        self.endframe   = bytes([0xff, 0xff, 0xff, 0xff])
        self.spi = SPI(1, SPI.MASTER, baudrate=45000000, polarity=0, phase=0,bits=8, firstbit=SPI.MSB)
        self.clearleds()

       
    #init empty self.buffer
    def clearleds(self):
        self.buffer = self.emptybuffer[:]

    @micropython.native    
    def setled(self, led, red=0, green=0, blue=0):
#        if (led > self.ledcount):
#            led=led % self.ledcount
#        
#        if (led < 0):
#            led = self.ledcount + led
        
        offset = led * 4
        self.buffer[offset] = 255  # equals a 1 or 0
        self.buffer[offset + 1] = blue
        self.buffer[offset + 2] = green
        self.buffer[offset + 3] = red

    def send(self):
        #self.spi.write(self.startframe + self.buffer + self.endframe)
        self.spi.send(self.startframe + self.buffer)
        
        
if __name__ == '__main__': 
    Dotty = DotStars(72)
    Dotty.send()
    bri = 1
    numpixels = 30          # Number of LEDs in strip
#    filename  = "hello.png" # Image file to load

	# Here's how to control the strip from any two GPIO pins:
	#datapin   = 23
	#clockpin  = 24
	#strip     = Adafruit_DotStar(numpixels, datapin, clockpin)

	#strip.begin()           # Initialize pins for output

	# Load image in RGB format and get dimensions:
#    print ("Loading...")
#    img       = Image.open(filename).convert("RGB")
#    pixels    = img.load()
    width     = 20
    height    = 20
#    print ("%dx%d pixels" % img.size)

	#if(height > strip.numPixels()): height = strip.numPixels()

	# Calculate gamma correction table, makes mid-range colors look 'right':
#    gamma = bytearray(256)
#    for i in range(256):
#        gamma[i] = int(pow(float(i) / 255.0, 2.7) * 255.0 + 0.5)

#    print ("Displaying...")
    while True:                              # Loop forever

    	for x in range(width):           # For each column of image...
         for y in range(height):  # For each pixel in column...
#             value = pixels[x, y]   # Read pixel in image
             Dotty.setled(y, # Set pixel in strip
             test.red[y*width+x],     # Gamma-corrected red
             test.green[y*width+x],     # Gamma-corrected green
             test.blue[y*width+x])     # Gamma-corrected blue
             Dotty.send()             # Refresh LED strip
	     #pyb.udelay(50)

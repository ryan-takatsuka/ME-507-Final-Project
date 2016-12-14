"""
Dotstars.py

Python module to control for APA102C ledstripes (Adafruit Dotstars) on the STM32 Discovery
Modified from the Wipy code: https://github.com/thilohille/wipy-dotstar
"""

# Import stuff
from pyb import SPI
import micropython


class DotStars:
    """
    DotStars class for communicating with the DotStars LEDs over SPI

    :atributes self: The external interrupt pin.
    :type name: int
    """

    # Initialize the class the SPI communication
    def __init__(self, leds):
        """
        This initializes the DotStars object by setting a buffer, and creating an SPI object.
        The start and end frames for the SPI communication are created, and the leds are cleared
        of values.

        :param leds: The number of LEDs
        :type name: int

        """
        self.ledcount = leds
        # create a buffer
        self.buffersize = self.ledcount * 4
        self.buffer = bytearray(self.ledcount * 4)
        self.emptybuffer = bytearray(self.ledcount * 4)
        for i in range(0, self.buffersize, 4):
            self.emptybuffer[i] = 0xff
            self.emptybuffer[i + 1] = 0x0
            self.emptybuffer[i + 2] = 0x0
            self.emptybuffer[i + 3] = 0x0
        # Start frame and endframe for the SPI communication (end frame is not
        # needed)
        self.startframe = bytes([0x00, 0x00, 0x00, 0x00])
        self.endframe = bytes([0xff, 0xff, 0xff, 0xff])
        # initialize SPI (needs to be at 45 MHz in order to maximize the speed.
        # This is the limiting factor for the system's speed)
        self.spi = SPI(1, SPI.MASTER, baudrate=45000000,
                       polarity=0, phase=0, bits=8, firstbit=SPI.MSB)
        self.clearleds()

    # empties the buffer and clears the LEDs
    def clearleds(self):
        """
        This method clears all the LEDs in the DotStar object

        """
        self.buffer = self.emptybuffer[:]

    # Compile this method into native code for the STM32 Discovery in order to
    # optimize the speed of the program
    @micropython.native
    # sets the LED with a specific red, green, and blue value
    def setled(self, led, red=0, green=0, blue=0):
        """
        This sets the led to the specified color

        :param led: The number of LEDs
        :type led: int
        :param red: The red value
        :type red: byte
        :param green: The green value
        :type green: byte
        :param blue: The blue value
        :type blue: byte

        """

        # Set the offset for the bytes to be sent over SPI
        offset = led * 4
        self.buffer[offset] = 255  # equals a 1 or 0
        self.buffer[offset + 1] = blue
        self.buffer[offset + 2] = green
        self.buffer[offset + 3] = red

    # Send the data over SPI (this takes about 100 us with a baud rate of 45
    # MHz)
    def send(self):
        """
        This method send the led data over SPI

        """
        self.spi.send(self.startframe + self.buffer)


# Used for debugging purposes
if __name__ == '__main__':
    Dotty = DotStars(72)
    Dotty.send()
    bri = 1
    numpixels = 72
    width = 20
    height = 20

    while True:                             # Loop forever
        for x in range(width):              # For each column of image...
            for y in range(height):         # For each pixel in column...
                Dotty.setled(y,             # Set pixel in strip
                            test.red[y * width + x],       # red value
                            test.green[y * width + x],     # green value
                            test.blue[y * width + x])      # blue value
                Dotty.send()                # Refresh LED strip
            pyb.udelay(50)

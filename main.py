"""
Created on Tue Dec  6 23:02:00 2016

@author: Ryan Takatsuka
"""

# Import stuff
from Dotstars import DotStars
import byte_picture
import pyb
import array

# create a DotStars class with 72 total LEDs
Dotty = DotStars(72)
Dotty.send()
# Specify the width and height of the image that will be imported
width     = 15 # [pixels]
height    = 24 # [pixels]
led_refresh_time = 900 # [microseconds]

# Converting the pixel list data into byte arrays
red_pixels = bytearray(byte_picture.red)
green_pixels = bytearray(byte_picture.green)
blue_pixels = bytearray(byte_picture.blue)

# Time arrays for calculating the maximum refresh rate of the microcontroller
times_array = array.array('L', [0]*(width*height))
times_for_SPIsend = array.array('L', [0]*(width*height))
diff_times_array = array.array('L', [0]*1000)
diff_times_row = array.array('L', [0]*1000)

# Variable that will be set during the ISR to determine timing
rotation_time = 0

# Handler method for the hall effect sensor
def hall_ISR(pin):
	global rotation_time
	rotation_time = millis()
	
# setup the interrupt on the PA0 pin on the STM32 Discovery board
interrupts = pyb.ExtInt(pyb.Pin.cpu.A0, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, hall_ISR)

# Method for finding the difference between elements in an array
def array_diff(in_array):
	diff_array = array.array('L',[0]*1000)
	for index, component in enumerate(in_array):
		if index<len(in_array)-1:
			diff_array[index] = (in_array[index+1] - in_array[index])
	return diff_array
			
# Method for printing the times recorded during the main loop
def timerTest():
	# Find the difference of the array of times
	diff_times_array = array_diff(times_array)
	
	# print the times it takes to refresh each led
	for row in range(height):
		for refresh_delay in range(width):
			print(str(diff_times_array[row*width+refresh_delay]), end=",")
		print()
		
	# print the time it takes to to the function Dotty.send()
	print('\n')
	for row in range(height):
		print(str(times_for_SPIsend[row]), end=",")
	print('\n')

# Main loop that updates the LEDs
while True:         
	for x in range(width):			# For each column of image...
		for y in range(height):		# For each pixel in column...
			Dotty.setled(y,			# Set pixel in strip
			red_pixels[y*width+x],	# red value
			green_pixels[y*width+x],	# green value
			blue_pixels[y*width+x])		# blue value
			
			# Dotty.send takes the most amount of time
			start = pyb.micros()
			Dotty.send()             # Refresh LED strip
			
			# Record the time it took to refresh the LEDs and to send the data over SPI
			times_for_SPIsend[y+x*width] = pyb.elapsed_micros(start)
			times_array[y*width+x] = pyb.micros()        

			# Wait a specified time to match the rotational speed of the system
			if pyb.elapsed_micros(start) > led_refresh_time:
				print ("refresh time is too fast. Error on pixel #" + str(y*width+x))
			while pyb.elapsed_micros(start) < led_refresh_time:
				pass

#	timerTest() - Can run this method to print the timing of the system

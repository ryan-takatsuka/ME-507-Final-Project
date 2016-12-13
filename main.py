"""
Created on Tue Dec  6 23:02:00 2016

@author: mecha27
"""
from Dotstars import DotStars
import byte_picture
import pyb
import sys
import array

Dotty = DotStars(72)
Dotty.send()
bri = 1
width     = 15
height    = 24
led_refresh_time = 900

# Converting the data into byte arrays was slower???
red_pixels = bytearray(byte_picture.red)
green_pixels = bytearray(byte_picture.green)
blue_pixels = bytearray(byte_picture.blue)

times_array = array.array('L', [0]*(width*height))
times_outer = array.array('L', [0]*(width*height))
times_row = array.array('L', [0]*(width*height))

diff_times_array = array.array('L', [0]*1000)
diff_times_outer = array.array('L', [0]*1000)
diff_times_row = array.array('L', [0]*1000)

#red_pixels = byte_picture.red
#green_pixels = byte_picture.green
#blue_pixels = byte_picture.blue

def hall_ISR(pin):
    print("printing")
    
extint = pyb.ExtInt(pyb.Pin.cpu.A0, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, hall_ISR)

def array_diff(in_array):
    diff_array = array.array('L',[0]*1000)
    for index, component in enumerate(in_array):
        if index<len(in_array)-1:
            diff_array[index] = (in_array[index+1] - in_array[index])
    return diff_array
            

def timerTest():
        
    diff_times_array = array_diff(times_array)
#    diff_times_row = array_diff(times_row)
    
    # print the times it takes to refresh each led
    for row in range(height):
        for refresh_delay in range(width):
            print(str(diff_times_array[row*width+refresh_delay]), end=",")
        print()
    
    # print the time it takes to update each column of leds    
    print('\n')
    for row in range(height):
        print(str(diff_times_row[row]), end=",")
        
    # print the time it takes to to the function Dotty.send()
    print('\n\n')
    for row in range(height):
        print(str(times_outer[row]), end=",")
      
    print('\n')
        
#    sys.exit()


while True:         
    for x in range(width):           # For each column of image...
        for y in range(height):  # For each pixel in column...
            Dotty.setled(y, # Set pixel in strip
            red_pixels[y*width+x],     # Gamma-corrected red
            green_pixels[y*width+x],     # Gamma-corrected green
            blue_pixels[y*width+x])     # Gamma-corrected blue
            
            # Dotty.send takes the most amount of time
            start = pyb.micros()
            Dotty.send()             # Refresh LED strip
            times_outer[y+x*width] = pyb.elapsed_micros(start)
            
            times_array[y+x*width] = pyb.micros()
#            times_array[y*width+x] = pyb.elapsed_micros(start)         

#            if pyb.elapsed_micros(start) > led_refresh_time:
#                print ("refresh time is too fast. Error on pixel #" + str(y*width+x))
#            while pyb.elapsed_micros(start) < led_refresh_time:
#                pass

        times_row[x] = pyb.micros()
#    timerTest()

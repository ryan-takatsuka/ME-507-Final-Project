"""
This creates 3 lists of RGB bytes in a separate file from the inputted image.
The inputted image can be any size and is reduced to the specified size of 15 X 24.
This size is picked because the LED strip being used is 24 pixels long and 15 frames per revolution is the 
highest resolution possible while still maintaining persistence of vision.
"""

# import the python imaging library
from PIL import Image

# open and rescale the image ('hello_5.jpeg' in this case)
img1 = Image.open("hello_5.jpeg").convert("RGB")  # open the original image and convert it to an array of RGB values
img2 = img1.resize((15, 24), Image.ANTIALIAS)  # resize the original image
img2.save('image_scaled.bmp')  # save the new resized image
print("Image size:  " + str(img1.size)) # print the new image size

# create lists of the red, green and blue data from the resized image
red = list(img2.getdata(band=0))
green = list(img2.getdata(band=1))
blue = list(img2.getdata(band=2))

# calculate the resaled image width and height
width, height = img2.size

# open or create a file to store the RGB list data of the image in
byte_picture = open('byte_picture.py', 'w+')

# write the red data of the image into the new file
byte_picture.write('red = [')  # start by declaring the variable and opening the brackets
for item in range(len(red)):
	byte_picture.write(str(red[item]))  # write the red value at the particular pixel to the file
	if (item != (len(red) - 1)):  # write a comma after the red data as long as it isn't the last entry in the list
		byte_picture.write(',')
else:
	byte_picture.write(']' + '\n')  # finish the list declaration and start a new line

# write the green data of the image into the new file
byte_picture.write('green = [')  # start by declaring the variable and opening the brackets
for item in range(len(green)):
	# write the green value at the particular pixel to the file
	byte_picture.write(str(green[item]))
	# write a comma after the green data as long as it isn't the last entry in the list
	if (item != (len(green) - 1)):
		byte_picture.write(',')
else:
	byte_picture.write(']' + '\n')  # finish the list declaration and start a new line

# write the blue data of the image into the new file
byte_picture.write('blue = [')  # start by declaring the variable and opening the brackets
for item in range(len(blue)):
	# write the blue value at the particular pixel to the file
	byte_picture.write(str(blue[item]))
	# write a comma after the blue data as long as it isn't the last entry in the list
	if (item != (len(blue) - 1)):
		byte_picture.write(',')
else:
	byte_picture.write(']' + '\n')  # finish the list declaration and start a new line

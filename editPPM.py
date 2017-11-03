# This is really just a collection of pixels and functions to operate on said pixels
# NOTE(clark): pixels are just tuples of 3 numbers between 0 and 255
# NOTE(clark): I was having a  bunch of fun and just implemented them all! 
import sys, os, fileinput, argparse, random

# Just a wrapper on pixel values
class pixel:

    # Sets the values and range checks. ezpz.  
    def __init__(self, vals):
        # Quick little range check
        if (0 <= vals[0] <= 255) and \
            (0 <= vals[1] <= 255) and \
            (0 <= vals[2] <= 255):
            self.r = vals[0]
            self.g = vals[1]
            self.b = vals[2]
        else:
            self.r = 0
            self.g = 0
            self.b = 0
            print("Incorrect ranges on pixel values.")


    # Returns a greyscale representation of image
    def to_greyscale(self):
        max_val = max(self.r, self.g, self.b);  
        return pixel((max_val, max_val, max_val))

    # Returns an inverted representation of image
    def to_inverted(self):
        return pixel((255 - self.r, 255 - self.g, 255 - self.b))

    # Returns a flattened version of the pixel
    def to_flat(self, color):
        if(color == 'r'):
            return pixel((0, self.g, self.b))
        elif(color == 'g'):
            return pixel((self.r, 0, self.b))
        elif(color == 'b'):
            return pixel((self.r, self.g, 0))
        

    # Returns a pixel with really contrasted values. 
    def to_contrast(self):
        contrast = 255
        factor = (259 * (contrast + 255)) / (255 * (259 - contrast))
        # compress the calculated values to the valid pixel range
        new_red   = min(max(int(factor * (self.r   - 128) + 128), 0), 255)
        new_green = min(max(int(factor * (self.g - 128) + 128), 0), 255)
        new_blue  = min(max(int(factor * (self.b  - 128) + 128), 0), 255)
        return pixel((new_red, new_green, new_blue))

    # Use other pixel values to influence this one
    def to_blur(self, factor):
        blur_blue = int( self.b * (0.5 / factor))
        blur_red = int( self.r * (0.5 / factor))
        blur_green = int( self.g * (0.5 / factor))
        return pixel((blur_red, blur_green, blur_blue))

    # returns a noisy version of the pixel
    def to_noise(self):
        new_red = max(0, min(255, self.r + random.randint(-100, 100)))
        new_green = max(0, min(255, self.g + random.randint(-100, 100)))
        new_blue = max(0, min(255, self.b + random.randint(-100, 100)))
        return pixel((new_red, new_green, new_blue))

    # reduce the pixels by a given factor
    # NOTE(clark): if I was exposing this API, I would range check this. 
    def reduce(self, factor):
        self.r = int(self.r * factor)
        self.g = int(self.g * factor)
        self.b = int(self.b * factor)

    # Adds the colors of one pixel to ours!
    def add(self, other):
        self.r = min(self.r + other.r, 255)
        self.g = min(self.g + other.g, 255)
        self.b = min(self.b + other.b, 255)

    # Turn to a string!
    def serialize(self):
        return str(self.r) + " " + str(self.g) + " " + str(self.b)

# Contains a small 2d matrix of pixel values and the operations to screw around with them. 
class ppmimage:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        # stuff it with a 'null' pixel for storage initialization
        self.pixels = [[0 for c in range(cols)] for r in range(rows)]

    def setpxl(self, pxl, row, col):
        if row >= self.rows or col >= self.cols:
            print("overflow")
            return

        self.pixels[row][col] = pxl

    # Getters and setters, I guess! I'm not sure if we even care about these in python. 
    def get_rows(self):
        return self.rows

    def get_cols(self):
        return self.cols

    # Flip all these along the 'x axis'
    def flip_horizontal(self):
        for r in range(self.rows):
            for idx in range(int(self.cols / 2)):
                # column tartget target
                ct = self.cols - 1 - idx
                # swap the pixels
                self.pixels[r][idx], self.pixels[r][ct] =  self.pixels[r][ct], self.pixels[r][idx]

    # Flips all the pixels across 'y axis'
    def flip_vertical(self): 
        for c in range(self.cols):
            for idx in range(int(self.rows / 2)):
                # row target target
                rt = self.rows - 1 - idx
                # swap the pixels
                self.pixels[idx][c], self.pixels[rt][c] =  self.pixels[rt][c], self.pixels[idx][c]


    # Applies the lambda to all pixels in list and stores them. 
    # Lambda is expected to take a pixel and return a pixel
    def transform(self, lamb):
        self.pixels = [[lamb(pxl) for pxl in row] for row in self.pixels]

    # trasform all pixels to their greyscale coutnerparts
    def greyscale(self):
        self.transform(lambda pxl: pxl.to_greyscale())

    # trasform all pixels to their greyscale coutnerparts
    def invert(self):
        self.transform(lambda pxl: pxl.to_inverted())

    # transforms all pixels to remove specified color
    def flatten(self, color):
        if(color == 'r' or color == 'R'):
            self.transform(lambda pxl: pxl.to_flat('r'))
        elif(color == 'g' or color == 'G'):
            self.transform(lambda pxl: pxl.to_flat('g'))
        elif(color == 'b' or color == 'B'):
            self.transform(lambda pxl: pxl.to_flat('b'))

    # transform all the pixels to REALLY contrasted versions of themselves
    def contrast(self):
        self.transform(lambda pxl: pxl.to_contrast())

    # Blurs the image horizontally
    def horizontal_blur(self):
        for row in self.pixels:
            for indx in range(len(row) - 1):
                row[indx].reduce(0.5)
                for shift in range(1, 51):
                    if shift + indx >= self.cols:
                        break 
                    # Blur the pixel with its right neighbor
                    row[indx].add(row[indx + shift].to_blur(shift))


    def random_noise(self):
        self.transform(lambda pxl: pxl.to_noise())

    def print_pixels(self):
        for r in self.pixels:
            for p in r:
                print(p.serialize())

    # returns the string in the PPM p3 format (ascii)
    def serialize(self):
        # File header
        ser_string = "P3\n" + str(self.cols) + " " + str(self.rows) + "\n255\n"
        # Serialize all the pixels
        for r in range(self.rows):
            for c in range(self.cols):
                ser_string += self.pixels[r][c].serialize() + " "
            ser_string += "\n"

        return ser_string




# ======================================
# Create argument parser for the program
# ======================================
# The argument parser
# TODO(clark): MAKE SURE THAT YOU GIVE A USER INTERFACE FOR THE PROGRAM
aparser = argparse.ArgumentParser(description = "Manipulates PPM images", prog = "editPPM", \
  usage='%(prog)s I -o O [optionsl args]\nexample: coolimage.ppm -o coolerimage.ppm -fh -b -a rb\n')
aparser.add_argument('input', metavar='I', type=str, help='The input ppm image for processing', nargs=1)
aparser.add_argument('-o', '--output', metavar='O', help='Output file for program. Ex: -o coolerimage.ppm', nargs=1, required=True)
aparser.add_argument('-fh', '--flip_horiz', help='Flips image horizontally', action='store_true')
aparser.add_argument('-fv', '--flip_vert', help='Flips image vertically', action='store_true')
aparser.add_argument('-g', '--greyscale', help='Converts image to greyscale', action='store_true')
aparser.add_argument('-i', '--invert', help='Inverts image colors', action='store_true')
aparser.add_argument('-a', '--flatten', type=str, choices='rgbRGB', metavar='RGB', help='Flattens colors of image [rgb]. Ex: -a rg', nargs=1)
aparser.add_argument('-b', '--horiz_blur', help='Blurs image horizontally. TAKES A LONG TIME', action='store_true')
aparser.add_argument('-c', '--contrast', help='Extreme contrast', action='store_true')
aparser.add_argument('-n', '--rand_noise', help='Random image noise', action='store_true')

# ======================================
# main code
# ======================================
# If we boot up the program with no args, prompt the user for some input.
if len(sys.argv) == 1:
    print('\n\n')
    aparser.print_help()
    args = aparser.parse_args(input("Enter command: ").split())
# If we boot up the program with flags, just parse them.  
else:
    args = aparser.parse_args()

# Read input
try:
    # read all the info from the given file
    with open(args.input[0]) as f:

        # Only process file if it is of P3 ppm type
        if(next(f).strip() != 'P3'):
            print('File is not of file type ppm P3')
            sys.exit(0)

        # Read rows and cols from line 2
        w, h = [int(x) for x in next(f).split()]

        # Only process PPM images with 255 color spread 
        
        if(next(f).strip() != '255'):
            print('File is not 255 color values')
            sys.exit(0)

        # Use this to initialize a pixmap
        pixmap = ppmimage(h, w);
        # Grab all the data from rest of file
        data = [[int(x) for x in line.split()] for line in f if not line.startswith('#')]

except:
    print('Input does not seem to exist or is corrupted')
    sys.exit(0)

#  flatten list
data = [x for sublist in data for x in sublist]

# Shove the data into the pixmap object
for row in range(pixmap.get_rows()):
    for col in range(pixmap.get_cols()):
        # Calculate 1d position for 2d pixmap from data
        index = (row * pixmap.get_cols() + col) * 3
        # represent pixel on pixmap
        # for some reason, pixmaps represent their pixels real strangely
        values = (data[index], data[index + 1], data[index + 2])
        pixmap.setpxl(pixel(values), row, col)


# Pretty easy to grasp. Just flip it by swapping all the pixels. 
if(args.flip_horiz):
    pixmap.flip_horizontal()

if(args.flip_vert):
    pixmap.flip_vertical();

if(args.greyscale):
    pixmap.greyscale();

if(args.invert):
    pixmap.invert();

# Flatten all the in args
if(args.flatten != None):
    print(list(args.flatten[0]))
    for color in list(args.flatten[0]):
        pixmap.flatten(color)

if(args.horiz_blur):
    pixmap.horizontal_blur()

if(args.contrast):
    pixmap.contrast()

if(args.rand_noise):
    pixmap.random_noise()


# If trying to write to a directory, make sure it exists
directory = os.path.dirname(os.path.abspath(args.output[0]))
if not os.path.exists(directory):
    os.makedirs(directory)

# Write the serialzation to the file. 
with open(args.output[0], "w+") as f:
    f.write(pixmap.serialize())


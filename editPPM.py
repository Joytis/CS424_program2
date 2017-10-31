# This is really just a collection of pixels and functions to operate on said pixels
# NOTE(clark): pixels are just tuples of 3 numbers between 0 and 255
import sys, fileinput, argparse

# Just a wrapper on pixel values
class pixel:

    # Sets the values and range checks. ezpz.  
    def __init__(self, vals):
        # Quick little range check
        if  (vals[0] >= 0 and vals[0] <= 255) and \
            (vals[1] >= 0 and vals[1] <= 255) and \
            (vals[2] >= 0 and vals[2] <= 255):
            self.r = vals[0]
            self.g = vals[1]
            self.b = vals[2]
        else:
            self.r = 0
            self.g = 0
            self.b = 0
            print("Incorrect ranges on pixel values.")

# Contains a small 2d matrix of pixel values and the operations to screw around with them. 
class ppmimage:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        # stuff it with a 'null' pixel for storage initialization
        self.pixels = [[pixel((0,0,0))] * rows] * cols

    def setpxl(self, pxl, row, col):
        if row >= self.rows or col >= self.cols:
            print("overflow")
            return

        self.pixels[row][col] = pxl


# ======================================
# Create argument parser for the program
# ======================================
# The argument parser
# TODO(clark): MAKE SURE THAT YOU GIVE A USER INTERFACE FOR THE PROGRAM
aparser = argparse.ArgumentParser(description = "Manipulates PPM images", prog = "editPPM", \
  usage='%(prog)s I -o O [optionsl args]')
aparser.add_argument('input', metavar='I', type=str, help='The input ppm image for processing', nargs=1)
aparser.add_argument('-o', '--output', metavar='O', help='Output file for program', nargs=1, required=True)
aparser.add_argument('-fh', '--flip_horiz', help='Flips image horizontally', action='store_true')
aparser.add_argument('-fv', '--flip_vert', help='Flips image vertically', action='store_true')
aparser.add_argument('-g', '--geryscale', help='Converts image to greyscale', action='store_true')
aparser.add_argument('-i', '--invert', help='Inverts image colors', action='store_true')
aparser.add_argument('-a', '--flatten', help='Flattens colors of image', action='store_true')
aparser.add_argument('-b', '--horiz_blur', help='Blurs image horizontally', action='store_true')
aparser.add_argument('-c', '--contrast', help='Extreme contrast', action='store_true')
aparser.add_argument('-n', '--rand_noise', help='Random image noise', action='store_true')

# ======================================
# main code
# ======================================
# If we boot up the program with no args, prompt the user for some input.
if len(sys.argv) is 1:
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
        # Grab all the data from rest of file
        data = [[int(x) for x in line.split()] for line in f]

except:
    print('Input does not seem to exist or is corrupted')
    sys.exit(0)




print(args.input, args.output, args.flip_horiz)

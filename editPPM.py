# This is really just a collection of pixels and functions to operate on said pixels
# NOTE(clark): pixels are just tuples of 3 numbers between 0 and 255
import fileinput, argparse

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
aparser = argparse.ArgumentParser(description = "Manipulates PPM images", prog = "editPPM", \
                                  usage='%(prog)s I -o O [optionsl args]')
aparser.add_argument('input', metavar='I', type=str, help='The input ppm image for processing', nargs=1)
aparser.add_argument('-o', '--output', metavar='O', help='Output file for program', nargs=1)

args = aparser.parse_args()

print(args.input, args.output)

# ======================================
# main code
# ======================================


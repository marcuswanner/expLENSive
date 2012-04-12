import sys, string
from common import readbmpfile
if len(sys.argv) > 1: infilename = sys.argv[1]
else: infilename = 'test.bmp'
if len(sys.argv) > 2: outfilename = sys.argv[2]
else: outfilename = 'bmptest.el2'
w, h, pixels = readbmpfile(infilename)
pixels = string.replace(pixels, '1', '2')
pixels = string.replace(pixels, '0', '1')
array = []
for i in range(h):
    array.append(pixels[i*w:(i+1)*w])
outfile = open(outfilename, 'w')
for i in array:
    outfile.write(i+'\n')
outfile.close()

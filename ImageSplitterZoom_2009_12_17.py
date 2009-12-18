#!/usr/bin/python

# Image Splitter
__version__ = '1.0'
__zoomifyVersion__ = '1.8' # for the ImageProperties.xml file

usage = """\
usage: %prog [options]
example: %prog -f image.tif

Image Splitter splits images and writes metadata in a format compatible with
the Zoomify software. Zoomify is a trademark of Zoomify, Inc. This program is
not authorized by Zoomify, Inc.

Note: You can type a space between the single-letter flag and the value."""

# PUBLIC DOMAIN NOTICE: The author(s) of this work dedicate it
# to the public domain. You may redistribute this code or modify
# it for any purpose. No attribution is necessary.

# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. THERE IS NO
# WARRANTY FOR THE SOFTWARE, TO THE EXTENT PERMITTED BY APPLICABLE
# LAW.

# Last modified: Nov. 23, 2004

from __future__ import division

import PIL.Image, os, sys, math, optparse, shutil

def debug(msg):
    if options.verbose == True:
        sys.stdout.write(msg)
        sys.stdout.flush()

def warning(msg):
    sys.stdout.write(msg)
    sys.stdout.flush()

from optparse import OptionParser

parser = OptionParser(usage=usage, version="%prog " + __version__)
parser.add_option("-f", "--file", dest="filename", metavar="FILE",
                  help="Input image for splitting. The recommended formats are TIFF, JPEG, PNG, and BMP. Formats listed at www.pythonware.com/library/pil/handbook/formats.htm may also be supported.", default=None)
parser.add_option("-d", "--dir", dest="dirName", metavar="DIR",
                  help="Output directory for image blocks and metadata. The default is the filename without the extension. Do not specify any slashes.", default=None)
parser.add_option("-b", "--block", dest="blockSize", default=256, metavar="PX",
                  help="Block size in pixels, default: 256. The value should be in multiples of 32 for JPEG processing. Try 512 or even higher for large, full-screen Flash objects.")
parser.add_option("-q", "--quality", dest="jpegQuality", default=85, metavar="QUALITY",
                  help="JPEG Quality of output blocks, from 1-100.")
parser.add_option("-s", "--silent",
                  action="store_false", dest="verbose", default=True,
                  help="Don't print processing messages to stdout")

(options, args) = parser.parse_args()

imageFile = options.filename

if imageFile == None or imageFile == "":
    print "An image file was not specified (option -f), printing --help...\n"
    
    parser.print_help()
    sys.exit()
elif not os.path.isfile(imageFile):
    raise IOError, "File '%s' does not exist." % (imageFile)

blockSize = int(options.blockSize)
imagesPerFolder = 256
jpegQuality = int(options.jpegQuality)

if options.dirName == None:
    dirName = imageFile[:imageFile.rfind(".")]
else:
    dirName = options.dirName
    
if os.path.isdir(dirName):
    warning("""\
WARNING: Directory '%s' already exists! Will proceed anyway,
but if the tile size has changed you must delete the directory
and re-run the program.\n
""" % dirName)
else:
    debug("Creating directory '%s'.\n" % dirName)
    os.mkdir(dirName)

debug("Block size: %dx%d pixels\n" % (blockSize, blockSize))
debug("Images per folder: %d\n" % imagesPerFolder)
debug("JPEG Quality: %d\n" % jpegQuality)
debug("\n")

debug("Loading original.\n")

# image Handle
iH = PIL.Image.open(imageFile)

width, height = iH.size
largestCoord = max(width, height)

# divide to find # of levels
levelsNeeded = 0
levelsDict = {}
currentSize = largestCoord
while True:
    currentSize /= 2
    levelsNeeded += 1
    if currentSize <= blockSize:
        break
        
debug("Levels needed: 0..%d\n" % levelsNeeded)

currentLevel = levelsNeeded

# split full-size image first
if not os.path.isdir("%s/TileGroup0" % dirName):
    os.mkdir("%s/TileGroup0" % dirName)

currentWidth = width
currentHeight = height

numBlocks = 0

while currentLevel >= 0:

    levelsDict[currentLevel] = {}

    if currentWidth != width or currentHeight != height:
        debug("Resizing original to %dx%d.\n" % (currentWidth, currentHeight))
        ciH = iH.resize((currentWidth, currentHeight), PIL.Image.ANTIALIAS)
    else:
        ciH = iH

    debug("Generating blocks for %dx%d image.\n" % (currentWidth, currentHeight))

    blocksWidth = int(math.ceil(currentWidth / blockSize))
    blocksHeight = int(math.ceil(currentHeight / blockSize))

    currentTileGroup = 0

    for blockVert in range(blocksHeight):
        levelsDict[currentLevel][blockVert] = {}
        for blockHoriz in range(blocksWidth):
            if not 'dimensions' in levelsDict[currentLevel]:
                levelsDict[currentLevel]['dimensions'] = (blocksWidth, blocksHeight)
            
            minCornerX = blockSize * blockHoriz
            minCornerY = blockSize * blockVert
            
            maxCornerX = min(minCornerX + blockSize, currentWidth)
            maxCornerY = min(minCornerY + blockSize, currentHeight)
            
            debug(".")
            
            #if (numBlocks % 256) == 0:
            #    currentTileGroup += 1
            #    os.mkdir("%s/TileGroup%d" % (dirName, currentTileGroup))
            
            levelsDict[currentLevel][blockVert][blockHoriz] = ciH.crop((minCornerX, minCornerY, maxCornerX, maxCornerY))
            levelsDict[currentLevel][blockVert][blockHoriz].load()
            levelsDict[currentLevel][blockVert][blockHoriz].save("%s/TileGroup0/%d-%d-%d.jpg" % (dirName, currentLevel, blockHoriz, blockVert), "JPEG", quality=jpegQuality)
            
            numBlocks += 1
            
            del levelsDict[currentLevel][blockVert][blockHoriz]


    debug("\n")
    debug("\n")

    # replace with reducer
    currentLevel -= 1
    currentWidth = int(math.floor(currentWidth / 2))
    currentHeight = int(math.floor(currentHeight / 2))

debug("Done writing %d blocks.\n" % (numBlocks))

debug("Writing pseudo-XML file.\n")

xmlFH = open("%s/ImageProperties.xml" % dirName, "wb")
xmlFH.write('<IMAGE_PROPERTIES WIDTH="%d" HEIGHT="%d" NUMTILES="%d" NUMIMAGES="1" VERSION="%s" TILESIZE="%d" />' % (width, height, numBlocks, __zoomifyVersion__, blockSize))
xmlFH.close()

if numBlocks > 256:
    debug("Rearranging tiles into separate directories.\n")
    reBlockCounter = 0
    reTileGroup = 0
    for level in range(levelsNeeded + 1):
        for yblock in range(levelsDict[level]['dimensions'][1]):
            for xblock in range(levelsDict[level]['dimensions'][0]):
                if (reBlockCounter % 256) == 0 and (reBlockCounter != 0):
                    reTileGroup += 1
                    if not os.path.isdir("%s/TileGroup%d" % (dirName, reTileGroup)):
                        os.mkdir("%s/TileGroup%d" % (dirName, reTileGroup))
                if reTileGroup > 0:
                    shutil.move("%s/TileGroup0/%d-%d-%d.jpg" % (dirName, level, xblock, yblock),
                            "%s/TileGroup%d/%d-%d-%d.jpg" % (dirName, reTileGroup, level, xblock, yblock))
                reBlockCounter += 1
                
debug("Image splitting completed.\n")
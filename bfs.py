#!/usr/bin/env python

import sys

from Queue import Queue
from PIL import Image
import time

start = (400,984)
end = (398,25)
start = (176,10)
end = (196,360)

def iswhite(value):
    if any(c < 225 for c in value):
        return False
    else:
        return True

def getadjacent(n):
    x,y = n
    return [(x-1,y),(x,y-1),(x+1,y),(x,y+1)]

def BFS(start, end, pixels):

    queue = Queue()
    queue.put([start]) # Wrapping the start tuple in a list

    while not queue.empty():

        path = queue.get()
        pixel = path[-1]

        if pixel == end:
            return path

        for adjacent in getadjacent(pixel):
            x,y = adjacent
            if iswhite(pixels[x,y]):
                pixels[x,y] = (127,127,127) # see note
                new_path = list(path)
                new_path.append(adjacent)
                queue.put(new_path)

    print "Queue has been exhausted. No answer was found."


if __name__ == '__main__':

    # invoke: python mazesolver.py <mazefile> <outputfile>[.jpg|.png|etc.]
    base_img = Image.open(sys.argv[1])
    base_pixels = base_img.load()

    start_time = time.time()
    path = BFS(start, end, base_pixels)

    print str(time.time() - start_time) + " seconds"
    print str(len(path)) + " path length"

    greys = 0
    for p in base_img.getdata():
        greys += 1
    print str(greys) + " greys"

    path_img = Image.open(sys.argv[1])
    path_pixels = path_img.load()

    for position in path:
        x,y = position
        path_pixels[x,y] = (255,0,0) # red
        base_pixels[x,y] = (255,0,0) # red

    path_img.save(sys.argv[2])
    base_img.save("p" + sys.argv[2])
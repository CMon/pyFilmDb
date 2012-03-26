#!/usr/bin/env python
import subprocess as sub
import shlex
import re
import sys

OUTPUT_PATH="/tmp/genGif/"
PNG_TEMP_PATH=OUTPUT_PATH + "png/"
GIF=OUTPUT_PATH + "output.gif"
N_FRAMES=20    # Number of frames for the final gif
GIF_WIDTH=200
GIF_HEIGHT=160
FFMPEG="/opt/local/bin/ffmpeg"
CONVERT="/opt/local/bin/convert"

def getDuration(filename):
    command_line = FFMPEG + " -t 1 -ss 1 -i '" + filename + "' -vcodec mjpeg -an -f rawvideo -vframes 1 -s " + str(GIF_WIDTH) + "x" + str(GIF_HEIGHT) + " -y '" + PNG_TEMP_PATH + "f001.png'"
    p = sub.Popen(shlex.split(command_line),stdout=sub.PIPE,stderr=sub.PIPE, close_fds=True)
    output, errors = p.communicate()
    time = re.compile("Duration: (\d+):(\d+):(\d+)").findall(errors)
    if len(time[0]) != 3:
        print "No duration found"
        return -1
    seconds = int(time[0][0]) * 3600 + int(time[0][1]) * 60 + int(time[0][2])
    print "Got a duration of " + str(seconds) + "s"
    return seconds

def getFrameSteps(filename):
    return (getDuration(filename)) / N_FRAMES

def generateGif(filename, step):
    print "Generate " + str(N_FRAMES) + " Frames"
    for i in range(2, N_FRAMES):
        cur_time = i * step
        command_line = FFMPEG + " -t 1 -ss " + str(cur_time) + " -i '" + filename + "' -vcodec mjpeg -an -f rawvideo -vframes 1 -s " + str(GIF_WIDTH) + "x" + str(GIF_HEIGHT) + " -y '" + PNG_TEMP_PATH + "f%(#)03d.png'" % { '#': i }
        p = sub.Popen(shlex.split(command_line),stdout=sub.PIPE,stderr=sub.PIPE, close_fds=True)
        p.wait()
    command_line = CONVERT + " -delay 70 -loop 0 '" + PNG_TEMP_PATH + "f*.png' '" + GIF + "'"
    p = sub.Popen(shlex.split(command_line), close_fds=True)
    p.wait()
    print "Done gif"

def cleanup():
    print "Delete files"
    command_line = "rm -f '" + PNG_TEMP_PATH + "'f*.png"
    p = sub.Popen(shlex.split(command_line), close_fds=True)
    p.wait()


testFile = ""
if (len(sys.argv) == 2):
    testFile = sys.argv[1]
elif len(sys.argv) != 2:
    print "Wrong usage"
    sys.exit()

steps = getFrameSteps(testFile)
generateGif(testFile, steps)
cleanup()
print "DONE"


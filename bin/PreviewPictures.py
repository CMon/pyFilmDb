import subprocess as sub
import shlex
import re
import sys


class PreviewPictures:
    outputPath    = "/tmp/genGif/"
    tempImagePath = outputPath + "png/"
    outputFile    = outputPath + "output.gif"
    nFrames       = 20 # Number of still images in the final gif
    gifWidth      = 200
    gifHeight     = 160
    ffmpegExecutable ="/opt/local/bin/ffmpeg"
    convertExecutable="/opt/local/bin/convert"

    def getDuration(self, filename):
        command_line = self.ffmpegExecutable + " -t 1 -ss 1 -i '" + filename + "' -vcodec mjpeg -an -f rawvideo -vframes 1 -s " + str(self.gifWidth) + "x" + str(self.gifHeight) + " -y '" + self.tempImagePath + "f001.png'"
        p = sub.Popen(shlex.split(command_line),stdout=sub.PIPE,stderr=sub.PIPE, close_fds=True)
        output, errors = p.communicate()
        time = re.compile("Duration: (\d+):(\d+):(\d+)").findall(errors)
        if len(time[0]) != 3:
            print "No duration found"
            return -1
        seconds = int(time[0][0]) * 3600 + int(time[0][1]) * 60 + int(time[0][2])
        print "Got a duration of " + str(seconds) + "s"
        return seconds

    def generateGif(self, filename):
        steps = self.__getFrameSteps(testFile)
        print "Generate " + str(self.nFrames) + " Frames"
        for i in range(2, self.nFrames):
            cur_time = i * steps
            command_line = self.ffmpegExecutable + " -t 1 -ss " + str(cur_time) + " -i '" + filename + "' -vcodec mjpeg -an -f rawvideo -vframes 1 -s " + str(self.gifWidth) + "x" + str(self.gifHeight) + " -y '" + self.tempImagePath + "f%(#)03d.png'" % { '#': i }
            p = sub.Popen(shlex.split(command_line), stdout=sub.PIPE, stderr=sub.PIPE, close_fds=True)
            p.wait()
        command_line = self.convertExecutable + " -delay 70 -loop 0 '" + self.tempImagePath + "f*.png' '" + self.outputFile + "'"
        p = sub.Popen(shlex.split(command_line), close_fds=True)
        p.wait()
        self.__cleanup()
        print "Done gif"

    def __getFrameSteps(self, filename):
        return (self.__getDuration(filename)) / self.nFrames

    def __cleanup(self):
        print "Delete files"
        command_line = "rm -f '" + self.tempImagePath + "'f*.png"
        p = sub.Popen(shlex.split(command_line), close_fds=True)
        p.wait()

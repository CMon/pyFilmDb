#!/usr/bin/env python
import os
import sys
from lxml import etree
import hashlib
from optparse import OptionParser
from PreviewPictures import PreviewPictures


homedir = os.path.expanduser("~")
parser = OptionParser()
parser.add_option("-b", "--basePath",             dest="basePath",        default=homedir+"/Downloads/", help="set the base directory from where all movies are searched")
parser.add_option("-c", "--createHash",           dest="createHash",      action="store_true",           help="create hash values for found movies")
parser.add_option("-d", "--updateDurations",      dest="updateDurations", action="store_true",           help="update duration fields for existing hashed files")
parser.add_option("-a", "--updateAnimatedImages", dest="updateAnimated",  default=None,                  help="create animated Preview gifs for those who do not have them, argument is the destination to place the gif")

AllowedExtensions=[
    ".wmv",
    ".mp4", ".m4v",
    ".flv", ".fid",
    ".avi",
    ".mpg", ".mpeg",
    ".mov",
    ".rmvb"
]

def getElemntText(element, tagname):
    text = element.xpath(tagname + "/text()")
    if len(text) == 0:
        return ""
    return text[0]

def newFileHashMapElement(hash, duration, animatedPreviewPath, stillPreviewPath):
    return dict([
        ('hash', hash),
        ('duration', duration),
        ('animatedPreviewPath', animatedPreviewPath),
        ('stillPreviewPath', stillPreviewPath)
    ])

def parseFixturesFile():
    fileHashMap = {}
    try:
        fixturesFile = open("fixtures.xml", "r+")
    except Exception,  e:
        print "Error: ", e
        return fileHashMap

    try:
        tree = etree.parse(fixturesFile)
    except Exception, e:
        print "parse Error: ", e
        return fileHashMap

    for element in tree.xpath("/fixtures/entry"):
        filename = element.xpath("relpath/text()")
        if len(filename) == 0:
            continue
        else:
            filename = filename[0]

        hash                = getElemntText(element, "hash")
        animatedPreviewPath = getElemntText(element, "animatedPreviewPath")
        duration            = getElemntText(element, "duration")
        stillPreviewPath    = getElemntText(element, "stillPreviewPath")


        fileHashMap[filename] = newFileHashMapElement(hash, duration, animatedPreviewPath, stillPreviewPath)

    fixturesFile.close()
    return fileHashMap

def writeFixturesFile(fileHashMap):
    print "Updating fixtures file do not disturb"
    root = etree.Element("fixtures")

    pp = PreviewPictures()
    ppWidth = pp.getWidth()
    ppHeight = pp.getHeight()

    for filename in fileHashMap.keys():
        entry = etree.SubElement(root, "entry")

        relpath = etree.SubElement(entry, "relpath")
        relpath.text = filename

        hash = etree.SubElement(entry, "hash")
        hash.text = str(fileHashMap[filename]['hash'])

        duration = etree.SubElement(entry, "duration")
        duration.text = str(fileHashMap[filename]['duration'])

        # TODO: fixme:
        # This will overwrite the Height and width, better would be the already stored values
        animatedPreviewPath = etree.SubElement(entry, "animatedPreviewPath", width=str(ppWidth), height=str(ppHeight))
        animatedPreviewPath.text = str(fileHashMap[filename]['animatedPreviewPath'])

        stillPreviewPath = etree.SubElement(entry, "stillPreviewPath", width=str(ppWidth), height=str(ppHeight))
        stillPreviewPath.text = str(fileHashMap[filename]['stillPreviewPath'])

    fixturesFile = open("fixtures.xml", "w+")
    fixturesFile.write(etree.tostring(root, pretty_print=True))
    fixturesFile.close()
    return

def listFiles(dir, files):
    basedir = dir
    subdirlist = []
    for item in os.listdir(dir):
        itemPath = os.path.join(basedir,item)
        if os.path.isfile(itemPath):
            fileName, fileExtension = os.path.splitext(itemPath)
            if fileExtension.lower() in AllowedExtensions:
                files.append(itemPath)
        elif os.path.isdir(itemPath):
            subdirlist.append(itemPath)
    for subdir in subdirlist:
        listFiles(subdir, files)

def calculateHash(fileName):
    print ("Calculating hash for ", fileName)
    m = hashlib.sha256()
    try:
        fd = open(fileName,"rb")
    except IOError:
        print "Unable to open the file in readmode:", fileName
        return "File not found"
    content = fd.readlines()
    fd.close()
    for eachLine in content:
        m.update(eachLine)
    return m.hexdigest()

def checkForDuplicates(fileHashMap):
    verifyList = []
    for file in fileHashMap.keys():
        h = fileHashMap[file]['hash']
        if h in verifyList:
            print "Duplicate Found: ", file
            continue
        verifyList.append(h)

    print "TODO: remove dupplicates"

## main methods

def incrementalHashGeneration(basePath, fileHashMap):
    files = []
    listFiles(basePath, files)

    print "Incremental Hash creation started"
    print " (Press CTRL+C to interrupt, already hashed movies will be stored)"

    try:
        for file in files:
            sha256 = ""
            fileBaseName = file[len(basePath):]
            if fileBaseName in fileHashMap.keys():
                if fileHashMap[fileBaseName]['hash'] == "":
                    sha256 = calculateHash(file)
                else:
                    sha256 = fileHashMap[fileBaseName]['hash']
                fileHashMap[fileBaseName]['hash'] = sha256
            else:
                sha256 = calculateHash(file)
                fileHashMap[fileBaseName] = newFileHashMapElement(sha256, 0, "", "")

    except KeyboardInterrupt, e:
        print "Interrupted hash creation storing files now"

    print "Finished creation of hashes, do not press CTRL+C now, because we are storing the file now"

    try:
        checkForDuplicates(fileHashMap)
    except Exception, e:
        # do not stop before writing
        print e
    writeFixturesFile(fileHashMap)

def updateDurations(basePath, fileHashMap):
    pp = PreviewPictures()

    print "Incremental update durations started"
    print " (Press CTRL+C to interrupt, completed movies will be stored)"
    somethingChanged = False
    try:
        for file in fileHashMap.keys():
            if fileHashMap[file]['duration'] == "":
                fullFilePath = basePath + "/" + file
                print "Setting Duration of " + fullFilePath
                fileHashMap[file]['duration'] = pp.getDuration(fullFilePath)
                somethingChanged = True
    except KeyboardInterrupt, e:
        print "Interrupted update of Durations storing files now"

    if somethingChanged:
        writeFixturesFile(fileHashMap)
    else:
        print "no Durations where updated"


def updateAnimatedGifs(basePath, pathForMediaStorage, fileHashMap):
    pp = PreviewPictures()

    print "Incremental update animated gifs started"
    print " (Press CTRL+C to interrupt, completed movies will be stored)"
    somethingChanged = False
    for file in fileHashMap.keys():
        if fileHashMap[file]['animatedPreviewPath'] == "":
            fullFilePath = basePath + "/" + file
            fileName = fileHashMap[file]['hash']
            print "Creating images for: " + fullFilePath

            outputAnimatedFile = pathForMediaStorage + fileName + ".gif"
            outputStillFile    = pathForMediaStorage + fileName + ".png"

            pp.generateGif(fullFilePath, outputAnimatedFile, outputStillFile)
            somethingChanged = True
            fileHashMap[file]['animatedPreviewPath'] = fileName + ".gif"
            fileHashMap[file]['stillPreviewPath']    = fileName + ".png"

    if somethingChanged:
        writeFixturesFile(fileHashMap)
    else:
        print "no Animated Preview Gifs where updated"

# Main program starts Here
(options, args) = parser.parse_args()

fileHashMap = parseFixturesFile()
basePath = options.basePath
actionPerformed = False

if options.createHash:
    incrementalHashGeneration(basePath, fileHashMap)
    actionPerformed = True

if options.updateDurations:
    updateDurations(basePath, fileHashMap)
    actionPerformed = True

if options.updateAnimated:
    if not os.path.isdir(options.updateAnimated):
        print "The argument for updateAnimatedImages has to be a directory"
    else:
        updateAnimatedGifs(basePath, options.updateAnimated, fileHashMap)
        actionPerformed = True

if not actionPerformed:
    parser.print_help()


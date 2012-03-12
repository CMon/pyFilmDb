#!/usr/bin/env python
import os
import sys
from xml.dom.minidom import Document
from lxml import etree
import hashlib

basePath = "/Users/twist/Downloads/"
if (len(sys.argv) == 2):
    basePath = sys.argv[1]
elif len(sys.argv) > 2:
    print "Wrong usage"
    sys.exit()

AllowedExtensions=[
    ".wmv",
    ".mp4", ".m4v",
    ".flv", ".fid",
    ".avi",
    ".mpg", ".mpeg",
    ".mov",
    ".rmvb"
]

def parseFixturesFile():
    fixturesFile = open("fixtures.xml", "r+")
    fileHashMap = {}
    try:
        tree = etree.parse(fixturesFile)
    except:
        print "parse Error"
        return fileHashMap

    for element in tree.xpath("/fixtures/entry"):
        filename = element.xpath("relpath/text()")
        if len(filename) == 0:
            continue
        else:
            filename = filename[0]

        hash = element.xpath("hash/text()")
        if len(hash) == 0:
            hash = ""
        else:
            hash = hash[0]

        fileHashMap[filename] = hash

    fixturesFile.close()
    return fileHashMap

def writeFixturesFile(fileHashMap):
    root = etree.Element("fixtures")

    for filename in fileHashMap.keys():
        entry = etree.SubElement(root, "entry")
        relpath = etree.SubElement(entry, "relpath")
        relpath.text = filename
        hash = etree.SubElement(entry, "hash")
        hash.text = fileHashMap[filename]

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
            if fileExtension in AllowedExtensions:
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
    sha256s = fileHashMap.values()
    verifyList = []
    for file in fileHashMap.keys():
        h = fileHashMap[file]
        if h in verifyList:
            print "Duplicate Found: ", file
            continue
        verifyList.append(h)

fileHashMap = parseFixturesFile()

files = []
listFiles(basePath, files)
for file in files:
    sha256 = ""
    fileBaseName = file[len(basePath):]
    if fileBaseName in fileHashMap.keys():
        if fileHashMap[fileBaseName] == "":
            sha256 = calculateHash(file)
        else:
            sha256 = fileHashMap[fileBaseName]
    else:
        sha256 = calculateHash(file)

    fileHashMap[fileBaseName] = sha256

checkForDuplicates(fileHashMap)
writeFixturesFile(fileHashMap)

print "Created fixtures file."

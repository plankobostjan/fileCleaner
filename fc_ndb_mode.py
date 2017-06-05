#!/usr/bin/python
import os
import time
import send2trash
import subprocess
import argparse
import sys
import getpass
import mysql.connector

class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def deleteEmptyLines():
    try:
        with open('.fileCleaner/defaults.txt','a+') as f:
            for line in f:
                if not line.isspace():
                    f.write(line)
        f.close()

    except Exception, e:
        print Bcolors.FAIL + repr(e) + Bcolors.ENDC
        print Bcolors.WARNING + "Program exited!" + Bcolors.ENDC
        sys.exit()

def deleteFile(path, endings, log, excluded_files):
    try:
        delete = 0
        log.write(time.strftime("\nOn %a %d.%m.%Y at %H:%M:%S:\n"))
        print time.strftime("On %a %d.%m.%Y at %H:%M:%S:")
        for filename in os.listdir(path):
            for f in excluded_files:
                if f != filename:
                    for ending in endings:
                       if  filename.endswith(ending):
                           send2trash.send2trash(path +'/' + filename)
                           log.write("{} in {} was send to trash.\n".format(filename, path))
                           print "{} in {} was send to trash.".format(filename, path)
                           delete += 1
                else:
                    print "File {} excluded.".format(f)
                    log.write("File {} excluded.\n".format(f))
        if delete == 0:
            print "No files were deleted in {}.".format(path)
            log.write("No files were deleted in {}.\n".format(path))
        log.close()

    except Exception, e:
        print Bcolors.FAIL + repr(e) + Bcolors.ENDC
        print Bcolors.WARNING + "Program exited!" + Bcolors.ENDC
        sys.exit()

def deleteContent(f):
    try:
        f.seek(0)
        f.truncate()
        
    except Exception, e:
        print Bcolors.FAIL + repr(e) + Bcolors.ENDC
        print Bcolors.WARNING + "Program exited!" + Bcolors.ENDC
        sys.exit()

def walkDirectoryTree(endings, log, path, excluded_files):
    if excluded_files is None:
        excluded_files = "none"
    try:
        log.write(time.strftime("\nOn %a %d.%m.%Y at %H:%M:%S:\n"))
        print time.strftime("On %a %d.%m.%Y at %H:%M:%S:")
        delete = 0
        for folderName, subfolders, filenames in os.walk(path):
            for filename in filenames:
                if filename not in excluded_files:
                        for ending in endings:
                           if  filename.endswith(ending):
                               send2trash.send2trash(folderName + '/' + filename)
                               log.write("{} in {} was send to trash.\n".format(filename, folderName))
                               print "{} in {} was send to trash.".format(filename, folderName)
                               delete += 1
                else:
                    print "File {} excluded.".format(filename)
                    log.write("File {} excluded.\n".format(filename))
        if delete == 0:
            print "No files were deleted."
            log.write("No files were deleted.\n")
        log.close()

    except Exception, e:
        print Bcolors.FAIL + repr(e) + Bcolors.ENDC
        print Bcolors.WARNING + "Program exited!" + Bcolors.ENDC
        sys.exit()

def defaults():
    try:
        endings = {".iso", ".gz", ".tar", ".zip", ".rar", ".7z", ".deb"}

        f = file(".fileCleaner/defaults.txt", 'w')
        deleteContent(f)
        for ending in endings:
            f.write(ending + "\n")
        f.close()

    except Exception, e:
        print Bcolors.FAIL + repr(e) + Bcolors.ENDC
        print Bcolors.WARNING + "Program exited!" + Bcolors.ENDC
        sys.exit()

def addEndings(endings_to_add):
    try:
        f = file(".fileCleaner/defaults.txt", "a+")
        data = f.read()
        print "Endings added:"
        for ending in endings_to_add:
            data += ending + "\n"
            print ending
        deleteContent(f)
        f.write(data)
        f.close()
        sys.exit()

    except Exception, e:
        print Bcolors.FAIL + repr(e) + Bcolors.ENDC
        print Bcolors.WARNING + "Program exited!" + Bcolors.ENDC
        sys.exit()

def getEndings():    
    try:
        deleteEmptyLines()
        f = file(".fileCleaner/defaults.txt", "r")
        data = f.read()
        rem = data.split("\n")
        data=''
        while '' in rem:
            rem.remove('')
        for el in rem[:-1]:
            data += el + "\n"
        data += rem[-1]
        data = data.split("\n")
        return data
        f.close()
        sys.exit()

    except Exception, e:
        print Bcolors.FAIL + repr(e) + Bcolors.ENDC
        print Bcolors.WARNING + "Program exited!" + Bcolors.ENDC
        sys.exit()

def deleteEndings(endings_to_remove):
    try:
        print "Endings removed:"
        for ending in endings_to_remove:
            f = open(".fileCleaner/defaults.txt", "r")
            lines = f.readlines()
            f.close()
            newLines = []
            print ending
            for line in lines:
                newLines.append(' '.join([word for word in line.split() if word != ending]))
            f = open(".fileCleaner/defaults.txt", "w")
            for line in newLines:
                f.write("{}\n".format(line))
            f.close()
            deleteEmptyLines()

    except Exception, e:
        f.close
        print Bcolors.FAIL + repr(e) + Bcolors.ENDC
        print Bcolors.WARNING + "Program exited!" + Bcolors.ENDC
        sys.exit()

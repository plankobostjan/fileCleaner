import os
import time
import send2trash
import subprocess
import argparse
import sys

def deleteEmptyLines():
    with open('defaults.txt','a+') as f:
        for line in f:
            if not line.isspace():
                f.write(line)
    f.close()
                
def deleteFile(path, endings, log):
    delete = 0
    log.write(time.strftime("\nOn %a %d.%m.%Y at %H:%M:%S:\n"))
    print time.strftime("On %a %d.%m.%Y at %H:%M:%S:")
    for filename in os.listdir(path):
        for ending in endings:
           if  filename.endswith(ending):
               send2trash.send2trash(path + filename)
               log.write("%s in %s was send to trash.\n" %(filename, path))
               print "%s in %s was send to trash." %(filename, path)
               delete += 1
    if delete == 0:
        print "No files were deleted."
        log.write("No files were deleted.\n")
               
def deleteEndings(items):
    print "Endings removed:"
    for item in items:
        f = open("defaults.txt", "r")
        lines = f.readlines()
        f.close()
        newLines = []
        print item
        for line in lines:
            newLines.append(' '.join([word for word in line.split() if word != item]))
        f = open("defaults.txt", "w")
        for line in newLines:
            f.write("{}\n".format(line))

def defaults():
    #default file endings to delete
    endings = {".iso", ".gz", ".tar", ".zip", ".rar", ".7z"}
    
    f = file("defaults.txt", 'w')
    deleteContent(f)
    for ending in endings:
        f.write(ending + "\n")
    f.close()
    
def deleteContent(f):
    f.seek(0)
    f.truncate()

def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--add-endings", nargs="+", type=str, help="Add file endings wich will be deleted.")
    parser.add_argument("-d", "--set-defaults", action="store_true",
                        help="Make file with default endings.")
    parser.add_argument("-l", "--list-endings", action="store_true", help="List all current endings.")
    parser.add_argument("-r", "--remove-endings", nargs="+", type=str, help="Remove endings.")
    parser.add_argument("-f", "--folder", type=str, help="Specify folder in wich you want to delete files.")
    args = parser.parse_args()

    if args.set_defaults is True:
        defaults()
        print "Defaults set!"
        sys.exit()

    if args.list_endings is True:
        deleteEmptyLines()
        f = file("defaults.txt", "r")
        data = f.read()
        rem = data.split("\n")
        data=''
        while '' in rem:
            rem.remove('')
        for el in rem:
            data += el + "\n"
        print "Current endings are:"
        print data
        f.close()
        sys.exit()
        
    if args.add_endings is not None:
        f = file("defaults.txt", "a+")
        data = f.read()
        print "Endings added:"
        for ending in args.add_endings:
            data += ending + "\n"
            print ending
        deleteContent(f)
        f.write(data)
        f.close()
        sys.exit()

    if args.remove_endings is not None:
        deleteEndings(args.remove_endings)
        deleteEmptyLines()
        sys.exit()

    if args.folder is not None:
        global folder
        folder = args.folder

def main():
    global folder
    folder = "/home/bostjan/Downloads/"
    arguments()
    
    try:
        f = file("defaults.txt", "r")
        data = f.read()
        if len(data) < 2:
            print "File with endings is empty.\nPlease generate defaults or add endings yourself."
            sys.exit()
        else:
            endings = data.split("\n")
            while '' in endings:
                endings.remove('')
        path = folder
        log = file("clearLog.txt", "a+")
        deleteFile(path, endings, log)
        log.close()
        f.close()
    except:
        print "Something went wrog!\nProgram exited!"
        print sys.exc_info()[0]
        sys.exit()

if __name__ == "__main__":
    main()

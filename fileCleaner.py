#!/usr/bin/python
import os
import time
import send2trash
import subprocess
import argparse
import sys
import getpass
import mysql.connector
import fc_ndb_mode
import fc_db_mode

class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#start of database mode methods 

#end of database mode methods

#start of methods for both modes

def arguments():
    parser = argparse.ArgumentParser()

    #arguments for both modes
    parser.add_argument("--add-endings", nargs="+", type=str, help="Add file endings wich will be deleted.")
    parser.add_argument("-d", "--set-defaults", action="store_true",
                        help="Set default endings.")
    parser.add_argument("--list-endings", action="store_true", help="List all current endings.")
    parser.add_argument("--remove-endings", nargs="+", type=str, help="Remove endings.")
    parser.add_argument("--walk", type=str, help="Walk thru directory tree and look for files to delete.")

    #database mode arguments
    parser.add_argument("--add-folders", nargs="+", help="Add folders in wich program will look for files.")
    parser.add_argument("--list-folders", action="store_true", help="List all current folders where progam will look for files.")
    parser.add_argument("--remove-folders", nargs="+", help="Remove specified folders from database")
    parser.add_argument("--add-excluded-folders", nargs="+", help="Add folders where program will not look for files.")
    parser.add_argument("--list-excluded-folders", action="store_true", help="List all excluded folders")
    parser.add_argument("--remove-excluded-folders", nargs="+", help="Remove specified excluded folders from database.")
    parser.add_argument("--add-excluded-files", nargs="+", help="Add files which won't be deleted.")
    parser.add_argument("--list-excluded-files", action="store_true", help="List all excluded files")
    parser.add_argument("--remove-excluded-files", nargs="+", help="Delete excluded files.")
    parser.add_argument("--create-database", action="store_true", help="Create database.")
    parser.add_argument("--database-mode", action="store_true", help="Use database for storing data for the program")

    #non-database mode mode arguments
    parser.add_argument("-f", "--folder", type=str, help="Specify folder in wich you want to delete files.")
    parser.add_argument("--exclude-file", type=str, nargs="+", help="Specify files to exclude.")

    args = parser.parse_args()
        
    #cases for database mode
    if args.add_folders is not None and args.database_mode == True:
        fc_db_mode.addFolders(args.add_folders)
        sys.exit()

    if args.list_folders == True and args.database_mode == True:
        folders = fc_db_mode.getFolders()
        print "Current folders are:"
        for folder in folders:
            print folder
        sys.exit()

    if args.remove_folders is not None and args.database_mode == True:
        fc_db_mode.removeFolders(args.remove_folders)
        sys.exit()

    if args.add_excluded_folders is not None and args.database_mode == True:
        fc_db_mode.addExcludedFolders(args.add_excluded_folders)
        sys.exit()

    if args.list_excluded_folders == True and args.database_mode == True:
        folders = fc_db_mode.getExcludedFolders()
        print "Current excluded folders are:"
        for folder in folders:
            print folder
        sys.exit()

    if args.remove_excluded_folders is not None and args.database_mode == True:
        fc_db_mode.removeExcludedFolders(args.remove_excluded_folders)
        sys.exit()

    if args.add_excluded_files is not None and args.database_mode == True:
        fc_db_mode.addExcludedFiles(args.add_excluded_files)
        sys.exit()

    if args.list_excluded_files == True and args.database_mode == True:
        excluded_files = fc_db_mode.getExcludedFiles()
        print "Current excluded files:"
        for excluded_file in excluded_files:
            print excluded_file
        sys.exit()

    if args.remove_excluded_files is not None and args.database_mode == True:
        fc_db_mode.removeExcludedFiles(args.remove_excluded_files)
        sys.exit()

    if args.create_database == True and args.database_mode == True:
        fc_db_mode.createDatabase()
        sys.exit()

    # if args.database_mode == True:
    #     try:
    #         folders = db_mode.getFolders()
    #         endings = db_mode.getEndings(args.database_mode)
    #         excluded_files = db_mode.getExcludedFiles()
    #         excluded_folders = db_mode.getExcludedFolders()
    #         log = file(".fileCleaner/clearLog.txt", "a+")
    #         db_mode.deleteFile(folders, endings, log, excluded_folders, excluded_files)
    #         log.close()
    #         sys.exit()

    #     except Exception, e:
    #         print Bcolors.FAIL + repr(e) + Bcolors.ENDC
    #         print Bcolors.WARNING + "Program exited!" + Bcolors.ENDC
    #         sys.exit()

    if args.add_endings is not None and args.database_mode == True:
        fc_db_mode.addEndings(args.add_endings)
        sys.exit()

    if args.set_defaults is True and args.database_mode == True:
        fc_db_mode.defaults()
        print "Defaults set!"
        sys.exit()

    if args.list_endings is True and args.database_mode == True:
        endings = fc_db_mode.getEndings()
        print "Current endings are:"
        for ending in endings:
            print ending
        sys.exit()

    if args.remove_endings is not None and args.database_mode == True:
        fc_db_mode.deleteEndings(args.remove_endings)
        sys.exit()

    if args.walk is not None and args.database_mode == True:
        endings = fc_db_mode.getEndings()
        log = file(".fileCleaner/clearLog.txt".format(user), "a+")
        excluded_files = args.exclude_file
        fc_db_mode.walkDirectoryTree(endings, log, args.walk, excluded_files)
        sys.exit()
        
    if len(sys.argv) == 2 and args.database_mode == True:
        log = file(".fileCleaner/clearLog.txt".format(user), "a+")
        folders = fc_db_mode.getFolders()
        endings = fc_db_mode.getEndings()
        excluded_folders = fc_db_mode.getExcludedFolders()
        excluded_files = fc_db_mode.getExcludedFiles()
        
        try:
            fc_db_mode.deleteFile(folders, endings, log, excluded_folders, excluded_files)
            log.close()

        except Exception, e:
            print Bcolors.FAIL + repr(e) + Bcolors.ENDC
            print Bcolors.WARNING + "Program exited!" + Bcolors.ENDC
            sys.exit()
        

    #cases for non-database mode
    if args.add_endings is not None and args.database_mode == False:
        fc_ndb_mode.addEndings(args.add_endings)
        sys.exit()

    if args.set_defaults is True and args.database_mode == False:
        fc_ndb_mode.defaults()
        print "Defaults set!"
        sys.exit()

    if args.list_endings is True and args.database_mode == False:
        endings = fc_ndb_mode.getEndings()
        print "Current endings are:"
        for ending in endings:
            print ending
        sys.exit()

    if args.remove_endings is not None and args.database_mode == False:
        fc_ndb_mode.deleteEndings(args.remove_endings)
        sys.exit()

    if args.walk is not None and args.database_mode == False:
        endings = fc_ndb_mode.getEndings()
        log = file(".fileCleaner/clearLog.txt".format(user), "a+")
        excluded_files = args.exclude_file
        fc_ndb_mode.walkDirectoryTree(endings, log, args.walk, excluded_files)
        sys.exit()
    
    if args.exclude_file is not None:
        excluded_files = args.exclude_file
    elif args.exclude_file is None:
        excluded_files = ["none"]
    
    if args.folder is not None:
        path = args.folder           
    else:
        path = "/home/{}/Downloads".format(user)

    if not len(sys.argv) > 1 and args.database_mode == False or args.exclude_file is not None or args.folder is not None:
        f = file(".fileCleaner/defaults.txt", "r")
        data = f.read()
        if len(data) < 2:
            print "File with endings is empty.\nPlease generate defaults or add endings yourself."
            sys.exit()
        else:
            endings = data.split("\n")
            while '' in endings:
                endings.remove('')
        log = file(".fileCleaner/clearLog.txt".format(user), "a+")
        try:
            fc_ndb_mode.deleteFile(path, endings, log, excluded_files)
            log.close()
            f.close()

        except Exception, e:
            print Bcolors.FAIL + repr(e) + Bcolors.ENDC
            print Bcolors.WARNING + "Program exited!" + Bcolors.ENDC
            sys.exit()
        
def main():
    try:
        global user
        user = getpass.getuser()
        arguments()
        sys.exit()

    except Exception, e:
        print Bcolors.FAIL + repr(e) + Bcolors.ENDC
        print Bcolors.WARNING + "Program exited!" + Bcolors.ENDC
        sys.exit()

if __name__ == "__main__":
    main()

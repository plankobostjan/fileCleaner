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

def createDatabase():
    try:
        print Bcolors.OKBLUE + "You are in database creation mode." + Bcolors.ENDC
        host = raw_input("Host: ")
        user = raw_input("User (with full privileges): ")
        passwd = getpass.getpass("Password for '{}': ".format(user))
        con = mysql.connector.connect(user=user, host=host, password=passwd)
        cursor = con.cursor()
        cursor.execute("show databases;")
        data = cursor.fetchall()
        for value in data:
            if value[0] == "fileCleaner":
                print "{}Database {} already exist!\nProgram exited!{}".format(Bcolors.WARNING, value[0], Bcolors.ENDC)
                sys.exit()
        cursor.execute("CREATE DATABASE fileCleaner;")
        cursor.execute("USE fileCleaner;")
        cursor.execute("Create table Endings (ending_id Int NOT NULL AUTO_INCREMENT, ending Varchar(10) NOT NULL, UNIQUE (ending_id), UNIQUE (ending), Primary Key (ending_id)) ENGINE = MyISAM;")
        cursor.execute("Create table Excluded_files (file_id Int NOT NULL AUTO_INCREMENT, filename Varchar(30) NOT NULL, UNIQUE (file_id), UNIQUE (filename), Primary Key (file_id)) ENGINE = MyISAM;")
        cursor.execute("Create table Excluded_folders (folder_id Int NOT NULL AUTO_INCREMENT, folder_name Varchar(100) NOT NULL, UNIQUE (folder_id), UNIQUE (folder_name), Primary Key (folder_id)) ENGINE = MyISAM;")
        cursor.execute("Create table Folders (folder_id Int NOT NULL AUTO_INCREMENT, path Varchar(100) NOT NULL, UNIQUE (folder_id), UNIQUE (path), Primary Key (folder_id)) ENGINE = MyISAM;")

    except Exception, e:
        print Bcolors.FAIL + repr(e) + Bcolors.ENDC
        print Bcolors.WARNING + "Program exited!" + Bcolors.ENDC
        sys.exit()
        
    try:
        print "{}Creating user 'scooter'...{}".format(Bcolors.OKBLUE, Bcolors.ENDC)
        cursor.execute("drop user scooter@{}".format(host))
        cursor.execute("flush privileges;")
        passwd = getpass.getpass("Choose password for user 'scooter': ")
        cursor.execute("Create user scooter@{} identified by '{}'".format(host, passwd))
        cursor.execute("GRANT insert, select, delete, alter on fileCleaner.* to scooter@{}".format(host))
        cursor.execute("FLUSH PRIVILEGES;")
        print "{}User 'scooter' successfully crated!{}".format(Bcolors.OKGREEN, Bcolors.ENDC)

    except Exception, e:
        print Bcolors.FAIL + repr(e) + Bcolors.ENDC
        print Bcolors.WARNING + "Program exited!" + Bcolors.ENDC
        sys.exit()

    try:
        print "{}Creating user 'rocky' (without password)...{}".format(Bcolors.OKBLUE, Bcolors.ENDC)
        cursor.execute("drop user rocky@{}".format(host))
        cursor.execute("flush privileges;")
        cursor.execute("Create user rocky@{}".format(host))
        cursor.execute("GRANT select on fileCleaner.* to rocky@{}".format(host))
        cursor.execute("FLUSH PRIVILEGES;")
        print "{}User 'rocky' successfully crated!{}".format(Bcolors.OKGREEN, Bcolors.ENDC)

    except Exception, e:
        print Bcolors.FAIL + repr(e) + Bcolors.ENDC
        print Bcolors.WARNING + "Program exited!" + Bcolors.ENDC
        sys.exit()
    
def removeExcludedFiles(excluded_files_to_remove):
    try:
        passwd = getpass.getpass("Password for 'scooter': ")
        con = mysql.connector.connect(user="scooter", host='localhost', password=passwd, database="fileCleaner")
        cursor = con.cursor()
        print "Removed files:"
        for excluded_file in excluded_files_to_remove:
            cursor.execute("DELETE FROM Excluded_files WHERE filename like '{}'".format(excluded_file))
            print excluded_file
        #sys.exit()

    except Exception, e:
        print Bcolors.FAIL + repr(e) + Bcolors.ENDC
        print Bcolors.WARNING + "Program exited!" + Bcolors.ENDC
        sys.exit()

def getExcludedFiles():
    try:
        con = mysql.connector.connect(user="rocky", host='localhost', database="fileCleaner")
        cursor = con.cursor()
        cursor.execute("SELECT filename FROM Excluded_files")
        data = cursor.fetchall()
        excluded_files = []
        for excluded_file in data:
            excluded_files.append(excluded_file[0].encode('utf-8'))
        return excluded_files

    except Exception, e:
        print Bcolors.FAIL + repr(e) + Bcolors.ENDC
        print Bcolors.WARNING + "Program exited!" + Bcolors.ENDC
        sys.exit()

def addExcludedFiles(excluded_files_to_add):
    try:
        passwd = getpass.getpass("Password for 'scooter': ")
        con = mysql.connector.connect(user="scooter", host='localhost', password=passwd, database="fileCleaner")
        cursor = con.cursor()
        print "Excluded files added:"
        for excluded_file in excluded_files_to_add:
            cursor.execute("INSERT INTO Excluded_files VALUES(0, '{}')".format(excluded_file))
            print excluded_files_to_add[0].decode('utf-8')
        #sys.exit()

    except Exception, e:
        print Bcolors.FAIL + repr(e) + Bcolors.ENDC
        print Bcolors.WARNING + "Program exited!" + Bcolors.ENDC
        sys.exit()

def removeExcludedFolders(excluded_folders_to_remove):
    try:
        passwd = getpass.getpass("Password for 'scooter': ")
        con = mysql.connector.connect(user="scooter", host='localhost', password=passwd, database="fileCleaner")
        cursor = con.cursor()
        print "Removed folders:"
        for folder in excluded_folders_to_remove:
            cursor.execute("DELETE FROM Excluded_folders WHERE folder_name like '{}'".format(folder))
            print folder
        #sys.exit()

    except Exception, e:
        print Bcolors.FAIL + repr(e) + Bcolors.ENDC
        print Bcolors.WARNING + "Program exited!" + Bcolors.ENDC
        sys.exit()

def getExcludedFolders():
    try:
        con = mysql.connector.connect(user="rocky", host='localhost', database="fileCleaner")
        cursor = con.cursor()
        cursor.execute("SELECT folder_name FROM Excluded_folders")
        data = cursor.fetchall()
        folders = []
        for folder in data:
            folders.append(folder[0].encode('utf-8'))
        return folders

    except Exception, e:
        print Bcolors.FAIL + repr(e) + Bcolors.ENDC
        print Bcolors.WARNING + "Program exited!" + Bcolors.ENDC
        sys.exit()

def addExcludedFolders(excluded_folders_to_add):
    try:
        passwd = getpass.getpass("Password for 'scooter': ")
        con = mysql.connector.connect(user="scooter", host='localhost', password=passwd, database="fileCleaner")
        cursor = con.cursor()
        print "Excluded folders added:"
        for folder in excluded_folders_to_add:
            cursor.execute("INSERT INTO Excluded_folders VALUES(0, '{}')".format(folder))
            print folder
        #sys.exit()

    except Exception, e:
        print Bcolors.FAIL + repr(e) + Bcolors.ENDC
        print Bcolors.WARNING + "Program exited!" + Bcolors.ENDC
        sys.exit()

def removeFolders(folders_to_remove):
    try:
        passwd = getpass.getpass("Password for 'scooter': ")
        con = mysql.connector.connect(user="scooter", host='localhost', password=passwd, database="fileCleaner")
        cursor = con.cursor()
        print "Removed folders:"
        for folder in folders_to_remove:
            cursor.execute("DELETE FROM Folders WHERE path like '{}'".format(folder))
            print folder
        #sys.exit()

    except Exception, e:
        print Bcolors.FAIL + repr(e) + Bcolors.ENDC
        print Bcolors.WARNING + "Program exited!" + Bcolors.ENDC
        sys.exit()

def addFolders(folders):
    try:
        passwd = getpass.getpass("Password for 'scooter': ")
        con = mysql.connector.connect(user="scooter", host='localhost', password=passwd, database="fileCleaner")
        cursor = con.cursor()
        print "Folders added:"
        for folder in folders:
            cursor.execute("INSERT INTO Folders VALUES(0, '{}')".format(folder))
            print folder
        #sys.exit()

    except Exception, e:
        print Bcolors.FAIL + repr(e) + Bcolors.ENDC
        print Bcolors.WARNING + "Program exited!" + Bcolors.ENDC
        sys.exit()     

def getFolders():
    try:
        con = mysql.connector.connect(user="rocky", host='localhost', database="fileCleaner")
        cursor = con.cursor()
        cursor.execute("SELECT path FROM Folders")
        data = cursor.fetchall()
        folders = []
        for folder in data:
            folders.append(folder[0].encode('utf-8'))
        return folders

    except Exception, e:
        print Bcolors.FAIL + repr(e) + Bcolors.ENDC
        print Bcolors.WARNING + "Program exited!" + Bcolors.ENDC
        sys.exit() 

def walkDirectoryTree(endings, log, path, excluded_floders, excluded_files):
    try:
        log.write(time.strftime("\nOn %a %d.%m.%Y at %H:%M:%S:\n"))
        print time.strftime("On %a %d.%m.%Y at %H:%M:%S:")
        delete = 0
        for folderName, subfolders, filenames in os.walk(path):
            if folderName + '/' in excluded_floders:
                print "{}Folder {} excluded.{}".format(Bcolors.WARNING, folderName + '/', Bcolors.ENDC)
                continue
            else:
                for filename in filenames:
                        if filename in excluded_files:
                            print "File {} excluded.".format(filename)
                            log.write("File {} excluded.\n".format(filename))
                            continue
                        else:
                            for ending in endings:
                               if  filename.endswith(ending):
                                   send2trash.send2trash(folderName + '/' + filename)
                                   log.write("{} in {} was send to trash.\n".format(filename, folderName))
                                   print "{} in {} was send to trash.".format(filename, folderName)
                                   delete += 1
                            
        if delete == 0:
            print "No files were deleted."
            log.write("No files were deleted.\n")
        log.close()

    except Exception, e:
        log.close
        print Bcolors.FAIL + repr(e) + Bcolors.ENDC
        print Bcolors.WARNING + "Program exited!" + Bcolors.ENDC
        sys.exit() 
        
def deleteFile(folders, endings, log, excluded_floders, excluded_files):
    try:
        delete = 0
        log.write(time.strftime("\nOn %a %d.%m.%Y at %H:%M:%S:\n"))
        print time.strftime("On %a %d.%m.%Y at %H:%M:%S:")
        for folder in folders:
            if folder in excluded_floders:
                print "Folder {} excluded.".format(folder)
                continue
            else:
                for filename in os.listdir(folder):
                    if filename in excluded_files:
                        print "File {} excluded.".format(filename)
                        log.write("File {} excluded.\n".format(filename))
                        continue
                    else:
                        for ending in endings:
                           if  filename.endswith(ending):
                               send2trash.send2trash(folder + filename)
                               log.write("{} in {} was send to trash.\n".format(filename, folder))
                               print "{} in {} was send to trash.".format(filename, folder)
                               delete += 1
                if delete == 0:
                    print "No files were deleted in {}".format(folder)
                    log.write("No files were deleted in {}\n".format(folder))
        log.close()
                
    except Exception, e:
        log.close()
        print Bcolors.FAIL + repr(e) + Bcolors.ENDC
        print Bcolors.WARNING + "Program exited!" + Bcolors.ENDC
        sys.exit()

def addEndings(endings_to_add):
    try:
        passwd = getpass.getpass("Password for 'scooter': ")
        con = mysql.connector.connect(user="scooter", host='localhost', password=passwd, database="fileCleaner")
        cursor = con.cursor()
        print "Endings added:"
        for ending in endings_to_add:
            cursor.execute("INSERT INTO Endings VALUES (0, '{}');".format(ending))
            print ending
        #sys.exit()

    except Exception, e:
        print Bcolors.FAIL + repr(e) + Bcolors.ENDC
        print Bcolors.WARNING + "Program exited!" + Bcolors.ENDC
        sys.exit()

def getEndings():
    try:
        con = mysql.connector.connect(user="rocky", host='localhost', database="fileCleaner")
        cursor = con.cursor()
        cursor.execute("SELECT ending FROM Endings;")
        data = cursor.fetchall()
        endings = []
        for ending in data:
            endings.append(ending[0].encode('utf-8'))
        cursor.close()
        con.close()
        return endings

    except Exception, e:
        print Bcolors.FAIL + repr(e) + Bcolors.ENDC
        print Bcolors.WARNING + "Program exited!" + Bcolors.ENDC
        sys.exit()
        
def deleteEndings(endings_to_remove):
    try:
        passwd = getpass.getpass("Password for 'scooter': ")
        con = mysql.connector.connect(user="scooter", host='localhost', password=passwd, database="fileCleaner")
        cursor = con.cursor()
        print "Endings removed:"
        for ending in endings_to_remove:
            cursor.execute("DELETE FROM Endings WHERE ending like '{}'".format(ending))
            print ending
        cursor.close()
        con.close()
        #sys.exit()

    except Exception, e:
        print Bcolors.FAIL + repr(e) + Bcolors.ENDC
        print Bcolors.WARNING + "Program exited!" + Bcolors.ENDC
        sys.exit()

def defaults():
    try:
        passwd = getpass.getpass("Password for 'scooter': ")
        con = mysql.connector.connect(user="scooter", host='localhost', password=passwd, database="fileCleaner")
        cursor = con.cursor()
        cursor.execute("DELETE FROM Endings;")
        cursor.execute("DELETE FROM Folders;")
        cursor.execute("ALTER TABLE Endings AUTO_INCREMENT = 1;")
        cursor.execute("ALTER TABLE Folders AUTO_INCREMENT = 1;")
        cursor.execute("INSERT INTO Endings VALUES (0, '.iso'), (0, '.gz'), (0, '.tar'), (0, '.zip'), (0, '.rar'), (0, '.7z'), (0, '.deb');")
        cursor.execute("INSERT INTO Folders VALUES (0, '/home/{}/Downloads/');".format(getpass.getuser()))
        print "{}Defaults generated!{}".format(Bcolors.OKGREEN, Bcolors.ENDC)
        cursor.close()
        con.close()
        #sys.exit()

    except Exception, e:
        print Bcolors.FAIL + repr(e) + Bcolors.ENDC
        print Bcolors.WARNING + "Program exited!" + Bcolors.ENDC
        sys.exit()

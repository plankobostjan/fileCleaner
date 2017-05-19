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
    
#start of non-database mode methods

def deleteEmptyLines():
    try:
        with open('defaults.txt','a+') as f:
            for line in f:
                if not line.isspace():
                    f.write(line)
        f.close()

    except Exception, e:
        print Bcolors.FAIL + repr(e) + Bcolors.ENDC
        print Bcolors.WARNING + "Program exited!" + Bcolors.ENDC
        sys.exit()

def deleteFileNonDatabase(path, endings, log, excluded_files):
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

def walkDirectoryTreeNonDatabase(endings, log, path, excluded_files):
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
                               print folderName + filename
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

#end of non-database mode methods

#start of database mode methods

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
        cursor.execute("IF EXISTS (select user from mysql.user where user = 'scooter') THEN drop user scooter@{}".format(host))
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
        cursor.execute("IF EXISTS drop user rocky@{} IF EXISTS".format(host))
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

def walkDirectoryTreeDatabase(endings, log, path, excluded_floders, excluded_files):
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
        
def deleteFileDatabase(folders, endings, log, excluded_floders, excluded_files):
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

#end of database mode methods

#start of methods for both modes

def addEndings(database_mode, endings_to_add):
    if database_mode == True:
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
    else:
        try:
            f = file("defaults.txt", "a+")
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

def getEndings(database_mode):
    if database_mode == True:
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
        
    else:
        try:
            deleteEmptyLines()
            f = file("defaults.txt", "r")
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

def deleteEndings(database_mode, endings_to_remove):
    if database_mode == True:
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

    else:
        try:
            print "Endings removed:"
            for ending in endings_to_remove:
                f = open("defaults.txt", "r")
                lines = f.readlines()
                f.close()
                newLines = []
                print ending
                for line in lines:
                    newLines.append(' '.join([word for word in line.split() if word != ending]))
                f = open("defaults.txt", "w")
                for line in newLines:
                    f.write("{}\n".format(line))
                f.close()
                    
        except Exception, e:
            f.close
            print Bcolors.FAIL + repr(e) + Bcolors.ENDC
            print Bcolors.WARNING + "Program exited!" + Bcolors.ENDC
            sys.exit()

def defaults(database_mode):
    if database_mode == True:
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

    else:
        try:
            endings = {".iso", ".gz", ".tar", ".zip", ".rar", ".7z", ".deb"}

            f = file("defaults.txt", 'w')
            deleteContent(f)
            for ending in endings:
                f.write(ending + "\n")
            f.close()

        except Exception, e:
            print Bcolors.FAIL + repr(e) + Bcolors.ENDC
            print Bcolors.WARNING + "Program exited!" + Bcolors.ENDC
            sys.exit()

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

    #cases for both modes
    if args.add_endings is not None:
        addEndings(args.database_mode, args.add_endings)
        sys.exit()

    if args.set_defaults is True:
        defaults(args.database_mode)
        print "Defaults set!"
        sys.exit()

    if args.list_endings is True:
        endings = getEndings(args.database_mode)
        print "Current endings are:"
        for ending in endings:
            print ending
        sys.exit()

    if args.remove_endings is not None:
        deleteEndings(args.database_mode, args.remove_endings)
        deleteEmptyLines()
        sys.exit()

    if args.walk is not None:
        endings = getEndings(args.database_mode)
        excluded_floders = getExcludedFolders()
        log = file("clearLog.txt", "a+")
        if args.database_mode == True:
            excluded_files = getExcludedFiles()
            walkDirectoryTreeDatabase(endings, log, args.walk, excluded_floders, excluded_files)
        else:
            excluded_files = args.exclude_file
            walkDirectoryTreeNonDatabase(endings, log, args.walk, excluded_files)
        sys.exit()
        
    #cases for database mode
    if args.add_folders is not None and args.database_mode == True:
        addFolders(args.add_folders)
        sys.exit()

    if args.list_folders == True and args.database_mode == True:
        folders = getFolders()
        print "Current folders are:"
        for folder in folders:
            print folder
        sys.exit()

    if args.remove_folders is not None and args.database_mode == True:
        removeFolders(args.remove_folders)
        sys.exit()

    if args.add_excluded_folders is not None and args.database_mode == True:
        addExcludedFolders(args.add_excluded_folders)
        sys.exit()

    if args.list_excluded_folders == True and args.database_mode == True:
        folders = getExcludedFolders()
        print "Current excluded folders are:"
        for folder in folders:
            print folder
        sys.exit()

    if args.remove_excluded_folders is not None and args.database_mode == True:
        removeExcludedFolders(args.remove_excluded_folders)
        sys.exit()

    if args.add_excluded_files is not None and args.database_mode == True:
        addExcludedFiles(args.add_excluded_files)
        sys.exit()

    if args.list_excluded_files == True and args.database_mode == True:
        excluded_files = getExcludedFiles()
        print "Current excluded files:"
        for excluded_file in excluded_files:
            print excluded_file
        sys.exit()

    if args.remove_excluded_files is not None and args.database_mode == True:
        removeExcludedFiles(args.remove_excluded_files)
        sys.exit()

    if args.create_database == True and args.database_mode == True:
        createDatabase()
        sys.exit()

    if args.database_mode == True:
        try:
            folders = getFolders()
            endings = getEndings(args.database_mode)
            excluded_files = getExcludedFiles()
            excluded_folders = getExcludedFolders()
            log = file("clearLog.txt", "a+")
            deleteFileDatabase(folders, endings, log, excluded_folders, excluded_files)
            log.close()
            sys.exit()

        except Exception, e:
            print Bcolors.FAIL + repr(e) + Bcolors.ENDC
            print Bcolors.WARNING + "Program exited!" + Bcolors.ENDC
            sys.exit()
        

    #cases for non-database mode
    if args.exclude_file is not None:
        excluded_files = args.exclude_file
    elif args.exclude_file is None:
        excluded_files = ["none"]
    
    if args.folder is not None:
        path = args.folder           
    else:
        user = getpass.getuser()
        path = "/home/{}/Downloads".format(user)

    if not len(sys.argv) > 1 and args.database_mode == False or args.exclude_file is not None or args.folder is not None:
        f = file("defaults.txt", "r")
        data = f.read()
        if len(data) < 2:
            print "File with endings is empty.\nPlease generate defaults or add endings yourself."
            sys.exit()
        else:
            endings = data.split("\n")
            while '' in endings:
                endings.remove('')
        log = file("clearLog.txt", "a+")
        try:
            deleteFileNonDatabase(path, endings, log, excluded_files)
            log.close()
            f.close()

        except Exception, e:
            print Bcolors.FAIL + repr(e) + Bcolors.ENDC
            print Bcolors.WARNING + "Program exited!" + Bcolors.ENDC
            sys.exit()
        
def main():
    try:
        arguments()
        sys.exit()

    except Exception, e:
        print Bcolors.FAIL + repr(e) + Bcolors.ENDC
        print Bcolors.WARNING + "Program exited!" + Bcolors.ENDC
        sys.exit()

if __name__ == "__main__":
    main()

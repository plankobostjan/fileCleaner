# fileCleaner
Program for cleaning files with specific endings.<br>
I've written this program for myself. Fell free to use it. <br>

<b>Warning</b><br>
I don't guarantee that the program will work for you. I'm also not responsible for the damage (lost files, ...) that this program my cause.

<b>Program does not permanently delete files. It sends them to trash.</b>

<b>First run</b><br>
  When you run the program for the first time, you need to run `python fileCleaner.py -d` to create file with file endings. File is created in the same folder where program itself is located.
  
<b>Logs</b><br>
Program creates a log file (clearLog.txt, same folder where program is located), where the data about deleted files is stored.
  
  <b>Two versions</b><br>
  There are two different versions of the program. One (fileCleaner.py) saves data to text files, the other one (fileCleaner_db.py) saves data to the database.<b>For database version, you need to have MariaDB server installed. To create database run</b> `python fileClesner_db.py --create-database`<b>.</b>
 
<b>Options for non-database version</b>

`-d, --set-defaults => Creates a file (defaults.txt) with preditermined file endigs.`<br>
`-l, --list-endings => Lists all endings, that are currently saved in endings file (defaults.txt)`<br>
`-a, --add-endings [ending, ...] => Adds endigs you enter to the defaults.txt file.`<br> 
`-r, --remove-endings [ending, ...] => Removes endings you enter from defaults.txt file.`<br>
`-f, --folder [folder] => Specify folder in wich you want to delete files (default: /home/USER/Downloads/)`<br>
`--walk => Walk thru directory tree, starting in specified folder (default: /home/USER/Downloads) and delete files.`

<b>Options for database version</b>

`-d, --set-defaults => Creates a file (defaults.txt) with preditermined file endigs.`<br>
`--list-endings => Lists all endings, that are currently saved in endings file (defaults.txt)`<br>
`--add-endings [ending ...] => Adds endigs you enter to the defaults.txt file.`<br> 
`-r, --remove-endings [ending ...] => Removes endings you enter from defaults.txt file.`<br>
`--add-folders [folder ...] => Add folders in wich program will look for files to the database.`<br>
`--walk [folder] => Walk thru directory tree and look for files to delete`<br>
`--list-folders => List all current folders where progam will look for files.`<br>
`--remove-folders [folder ...] => Remove specified folders from the database.`<br>
`--add-excluded-folders [folder ...] => Add folders where program will not look for files to the database.`<br>
`--list-excluded-folders => List all excluded folders.`<br>
`--remove-excluded-folders => Remove specified excluded folders from the database.`<br>
`--add-excluded-folders => Add files which won't be searched to the database.`<br>
`--list-excluded-files => List all excluded files.`<br>
`--remove-excluded-file => Delete specified files form the database.`<br>
`--create-database => Create database in wich data will be stored`<br>

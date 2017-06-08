# fileCleaner
Program for cleaning files with specific endings.<br>
I've written this program for myself. Fell free to use it.<br>
Some options are added just because of my curiosity.<br>

<b>Warning</b><br>
I don't guarantee that the program will work for you. I'm also not responsible for the damage (lost files, ...) that this program my cause.

<b>Program does not permanently delete files. It sends them to trash.</b>

<b>First run</b><br>
  When you run the program for the first time, you need to run it with `--set-defaults` option.
  
<b>Logs</b><br>
Program creates a log file (clearLog.txt, same folder where program is located), where the data about deleted files is stored.
  
<b>Two modes</b><br>
 There are two different modes of the program. By default, data for the program (endings) are stored in text files. But, if you want, you can run program with `--database-mode` option. If you do so, all the data will be saved in the database. For the database mode, you need to have MariaDB server installed. To create database run `python fileCleaner_db.py --create-database`.
  
<b>Options for both modes</b><br>
`-d, --set-defaults => Creates a file (defaults.txt) with preditermined file endigs.`<br>
`--list-endings => Lists all endings, that are currently saved in endings file (defaults.txt)`<br>
`--add-endings ENDING ... => Adds endigs you enter to the defaults.txt file.`<br> 
`--remove-endings ENDING ... => Removes endings you enter from defaults.txt file.`<br>
`--walk FOLDER => Walk thru directory tree, starting in specified folder (default: /home/USER/Downloads) and delete files.`
 
<b>Options specific to non-database mode</b><br>
`-f, --folder FOLDER => Specify folder in wich you want to delete files (default: /home/USER/Downloads/)`<br>
`--exclude-file FILE ... => Specify files wich will be excluded.`

<b>Options specific to the database mode</b><br>
`--add-folders FOLDER ... => Add folders in wich program will look for files to the database.`<br>
`--list-folders => List all current folders where progam will look for files.`<br>
`--remove-folders FOLDER ... => Remove specified folders from the database.`<br>
`--add-excluded-folders FOLDER ... => Add folders where program will not look for files to the database.`<br>
`--list-excluded-folders => List all excluded folders.`<br>
`--remove-excluded-folders => Remove specified excluded folders from the database.`<br>
`--add-excluded-folders => Add files which won't be searched to the database.`<br>
`--list-excluded-files => List all excluded files.`<br>
`--remove-excluded-file => Delete specified files form the database.`<br>
`--create-database => Create database in wich data will be stored`<br>

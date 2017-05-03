# fileCleaner
Program for cleaning files with specific endings.
I've written this program for myself.<br>
Fell free to use this program.
<b>BUT:</b><br>
  I don't guarantee that it will work for you. I'm also not responsible for damage (lost files, ...) that this program my cause.

Program does not permanently delete files. It sends them to trash.

<b>First run</b><br>
  When you run the program for the first time, you need to run <b>python fileCleaner.py -d</b> to create file with file endings. File is create in same folder where program itself is located.
  
<b>Logs</b><br>
Program creates a log file (same folder where program is located), where the data about deleted files is stored.
 
<b>Options</b>

  -d, --set-defaults =>
          Creates a file (defaults.txt) with preditermined file endigs.
          
  -l, --list-endings =>
          Lists all endings, that are currently saved in endings file (defaults.txt).

  -a, --add-endings [ending, ...] =>
          Adds endigs you enter to the defaults.txt file.
          
  -r, --remove-endings [ending, ...] =>
          Removes endings you enter from defaults.txt file.
               
  -f, --folder [folder] =>
          Specify folder in wich you want to delete files (default: /home/bostjan/Downloads)

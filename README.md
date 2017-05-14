# fileCleaner
Program for cleaning files with specific endings.
I've written this program for myself.<br>
Fell free to use this program. <br>

<b>Warning</b><br>
I don't guarantee that it will work for you. I'm also not responsible for damage (lost files, ...) that this program my cause.

<b>Program does not permanently delete files. It sends them to trash.</b>

<b>First run</b><br>
  When you run the program for the first time, you need to run <b>python fileCleaner.py -d</b> to create file with file endings. File is created in the same folder where program itself is located.
  
<b>Logs</b><br>
Program creates a log file (clearLog.txt, same folder where program is located), where the data about deleted files is stored.
 
<b>Options</b>

`-d, --set-defaults => Creates a file (defaults.txt) with preditermined file endigs.`<br>
`-l, --list-endings => Lists all endings, that are currently saved in endings file (defaults.txt)`<br>
`-a, --add-endings [ending, ...] => Adds endigs you enter to the defaults.txt file.`<br> 
`-r, --remove-endings [ending, ...] => Removes endings you enter from defaults.txt file.`<br>
`-f, --folder [folder] => Specify folder in wich you want to delete files (default: /home/bostjan/Downloads/)`<br>
`--walk => Walk thru directory tree, starting in specified folder (default: /home/USER/Downloads) and delete files.`

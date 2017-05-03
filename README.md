# fileCleaner
Program for cleaning files with specific endings.
I've written this program for myself.<br>
Fell free to use this program.
<b>BUT:</b><br>
  I don't guarantee that it will work for you. I'm also not responsible for damage (lost files, ...) that this program my couse.

Program does not permanently delete files. It send them to trash.

<b>First run</b><br>
  When you run the program for the first time, you need to run <b>python fileCleaner.py -d</b> to create file with file endings.
 
<b>Options</b>

  -d, --set-defaults =>
          Creates a file with preditermined file endigs wich will be deleted.
          
  -l, --list-endings =>
          Lists all endings, that are currently saved in endings file (defaults.txt).

  -a, --add-endings [ending, ...] =>
          Adds endigs you enter to the defaults.txt file.
          
  -r, --remove-endings [ending, ...] =>
          Removes endings you enter from defaults.txt file.<br><b>Warning</b><br>
          There is a bug with this option (-r, --remove-endings)! If you try to remove more that one ending at a time, endings will be duplicated.
               
  -f, --folder [folder] =>
          Specify folder in wich you want to delete files (default: /home/bostjan/Downloads)

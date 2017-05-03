# fileCleaner
Program for cleaning files with specific endings.
I've written this program for myself
Fell free to use this program.
<b>BUT:</b>
  I don't guarantee that it will work for you. I'm also not responsible to damage (lost files) that this program my couse.

Program does not peranently delete files. It send them to trash.

<b>First run</b>
  When you run the program for the first time, you need to run <b>python fileCleaner.py -d</b> to create file with file endings which will be deleted.
 
<b>Options</b>
  -d, --set-defaults 
          Creates a file with preditermined file endigs wich will be deleted.
          
  -l, --list-endings 
          Lists all endings, that are currently saved in endings file (defaults.txt).

  -a, --add-endings [ending, ...]
          Adds endigs you enter to the defaults.txt file.
          
  -r, --remove-endings [ending, ...]
          Removes endings you enter from defaults.txt file.
          <b>Warning</b>
               There is a bug with this option! If you try to remove more that one ending at a time, endings will be duplicated.
               
  -f, --folder [folder]
          Specify folder in wich you want to delete files (default: /home/bostjan/Downloads)

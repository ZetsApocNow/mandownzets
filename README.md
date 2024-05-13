My own edits to make file downloading work, no idea how to code but it works well. Is aided by File Juggler program to move cbz files into their own folders in a folder called Moved Files. I only want use of it to download comics so any use outside of the command I have below will probably error out. Spent 2 days straight on this trying to get it to work how I wanted, again I'm not a coder, just a prodder.



Make sure penis.bat is in this folder - V:\Jellyfin\All Files\Graphic Novels
Run File Juggler, turn on "move cbz 2"
shift right click in this folder to open Powershell

type in
mandown get -c cbz -b -r 
then paste url

Files will firstly go to Graphic Novels in a folder, then will be converted to cbz and then File Juggler will move then to their own folders inside Moved Files




If File Juggler rule is missing,

Monitor - Graphic Novels
If - file extension contains text cbz
Then - Run command - start "" "V:\Jellyfin\All Files\Graphic Novels\penis.bat"



If penis.bat is missing make a new one with the below code

@echo off
setlocal enabledelayedexpansion

set "sourceFolder=V:\Jellyfin\All Files\Graphic Novels"
set "destinationFolder=V:\Jellyfin\All Files\Graphic Novels\Moved Files"

for %%F in ("%sourceFolder%\*.cbz") do (
    set "filename=%%~nF"
    setlocal enabledelayedexpansion
    for /f "tokens=1 delims=-" %%A in ("!filename!") do (
        set "newFolder=%%A"
        set "newFolder=!newFolder:~0,-1!"
        if not exist "!destinationFolder!\!newFolder!" (
            md "!destinationFolder!\!newFolder!" 2>nul
        )
        move "%%F" "!destinationFolder!\!newFolder!\"
    )
    endlocal
)

echo All cbz files have been moved successfully!

exit

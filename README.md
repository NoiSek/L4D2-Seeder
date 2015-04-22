# L4D2-Seeder
A script to seed L4D2 servers with users. Currently does *not* work with 
Linux. Makes use of [Python-Valve](https://github.com/Holiverh/python-valve)

**USE AT YOUR OWN RISK, YOUR ACCOUNT MAY BE VAC BANNED.**

## Requirements

 - Windows
 - Steam
 - L4D2 Client (Not server)
 - Python 2 / 3

## Why would I use this?
As of the time of writing, Valve sends users looking to find a match in L4D2 to servers already occupied by at least one player. This script will connect to a list of servers one by one, and disconnect once there is a user connected, thereby seeding the server so that Valve will continue filling it with users.

## How to
To use this, edit the servers.lst to include all of the servers you with the script to cycle through. It will launch L4D2 using your Steam.exe and L4D2's AppID, edit the path_to_steam within run.py if your Steam install location is non-standard, otherwise run and forget.

L4D2 should run regardless of where you have it installed, as long as Steam itself is located at it's default location in your Program Files directory.

As of [699f84](https://github.com/NoiSek/L4D2-Seeder/commit/699f847608bab5a9c71cbd31131a9cfb63d17b4a), L4D2 launches in true textonly mode and no longer flashes to fullscreen before collapsing to the command prompt. As the game is still launched and then terminated on every connect, you may want to run this on a machine where you will not be interrupted by it.

## Hiding L4D2 windows
It is now possible to hide L4D2 windows on Windows machines. This is not available by default and requires that you download an external library.

To Use:
- Download PyWin32 from [here](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pywin32). Then navigate to your downloads directory and run ```pip install <name of file>```. Where ```<name of file>``` is the .whl you received.
- run ```python hide_launcher.py```
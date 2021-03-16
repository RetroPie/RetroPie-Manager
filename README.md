
# Retropie-Manager-Plus
# About
This an enhanced RetroPie-Manager fork.
Original RetroPie-Manager repository: https://github.com/RetroPie/RetroPie-Manager

# Features
With Retropie-Manager you can
- Monitor the system health and disk space
- Edit the Emulation Station config file
- Edit the RetroArch config file
- Edit the autostart.sh script
- View the Emulation Station log file
- Manage your BIOS files
- Manage your ROMS

# Limitations
- It doesn't support subdirectories at ROMs dir (as reported [here](https://github.com/botolo78/RetroPie-Manager/issues/5))

# Install
**Dependencies on Raspberry Pi**

```sh
sudo apt-get install virtualenv python-dev
```

**Dependencies on Ubuntu-based Linux distribution**

```sh
sudo apt-get install python-virtualenv python-dev
```

**Installing RetroPie-Manager**
```sh
cd
git clone https://github.com/NicholasBerryman/RetroPie-Manager-Plus.git
cd RetroPie-Manager-Plus
make install
```

# Usage

You must be at the RetroPie-Manager's directory to use the `rpmanager.sh` like in the examples below.

**Start**
```sh
./rpmanager.sh --start
```
Open your browser and go to **http://your_retropie_ip:8000/**

**Stop**
```sh
./rpmanager.sh --stop
```

**More options**
```sh
[prompt]$ ./rpmanager.sh --help
Usage: rpmanager.sh OPTIONS

The OPTIONS are:

-h|--help           print this message and exit

--start             start the RetroPie-Manager

--stop              stop the RetroPie-Manager

--isrunning         show if RetroPie-Manager is running and the
                    listening port and exit

--log               save the log messages (optional, default: not save log
                    messages, only works with --start)

-u|--user USER      start RetroPie-Manager as USER (only available for
                    privileged users, only works with --start, USER must 
                    be a RetroPie user)

The --start and --stop options are, obviously, mutually exclusive. If the
user uses both, only the first works.

```


# Autostart
To make Retropie-Manager to start with your RetroPie machine simply add it as a reboot Cronjob.
First, run
```crontab -e```
Then, add the following line to the end of the file:
```
@reboot /opt/retropie/supplementary/retropie-manager-plus/rpmanager.sh --start
```
# Update
```sh
sudo kill -9 $(pgrep -f RetroPie-Manager)
cd 
cd Retropie-Manager
make clean
git reset --hard HEAD
git pull
make install
```

# Reinstall
```sh
sudo kill -9 $(pgrep -f RetroPie-Manager)
cd 
rm -rf Retropie-Manager
git clone https://github.com/botolo78/RetroPie-Manager.git
cd RetroPie-Manager
make install
```

# Additions to the base RetroPie-Manager:
- Adds .pbp as a valid PSX ROM extension (DONE)
- Fixes PSX BIOS hashes (DONE)
- Increases max uploadable rom size to 10GB from 256MB (DONE)
- Adds real-time updating to Monitoring page (MOSTLY DONE)
  * Updates all values on the monitoring screen every 3 seconds (DONE)
  * Updates file system table if devices are added/removed e.g. a USB (TODO)
  * **Requires Javascript**
- Adds custom-data monitoring (TODO)
- Allows rom sub-directories (TODO)
- Re-introduces save management (TODO)
- Migrate to Python 3 (TODO)

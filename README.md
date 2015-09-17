# Scope
There is many privacy and secure communication tools that worth to use to help user at risk to do his works and protect him from the adversary. The problem here is that user needs to choose and install all these tools manually and this is a challenging task for no-tech user. So it is helpful to build a solution that automates this task and guide the user through simple steps.

# Concept
We proposed to build a tool that help user at risk in installing important privacy and secure communication tools that help him to do his works with a lower risk.

FlyRodCrosby is a cross-platform automated installer for most of the privacy and secure communication tools. It currently handles:
- GPG
- Tor Browser
- Thunderbird
- Enigmail
- TorBirdy
- Jitsi

FlyRodCrosby will download the listed tools and verify the pgp signature then install them. 


# Packages / Dependencies

### Prerequisites
- Python 2.7
- pip
- wxPython (Windows, Linux), PyQt4 (Mac)
- Git

### Install python modules
- After installing the Prerequisites you can clone this repository:
```
$ git clone https://github.com/AccessNow/FlyRodCrosby
$ cd FlyRodCrosby
$ sudo pip install -r requirements.txt 
```

# How to use ?
- Switch to the appropriate branch:
  - master for Windows OS
  - frc-linux for Linux OS
  - frc-osx for Mac OS
```
$ git checkout <branch>
```
- Now you can run the application using this command:
```
$ python frc-gui.py 
```
Note: You need to run it as root on Linux version

# How to contibute ?
```
$ git clone https://github.com/AccessNow/FlyRodCrosby
```
And start coding :D !!

# How to build

To build FlyRodCrosby from source, install PyInstaller and type

$ pyinstaller frc-gui.py --onefile

# TODO
Want to contribute? Here is a short TODO list of things that aren't implemented for this application that would be nice:

- Onionshare
- The Commotion wireless client or some mesh network client software
- Some kind of instructional materials that the user can read while they download their apps.
- One of those Mumble Push-To-Talk apps.


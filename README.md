# DSLSpeedMeter
Display current internet down-/upload speed on LED strip

 +--------------------------+
 | How to setup Speed Meter |
 +--------------------------+
 
 (Rough instructions for Setup from Windows. Linux Users will know how to adapt anyway :P)
 
 Get
 - a Blinky Tape (e.g. 60 LEDs)
 - a raspberry pi (e.g. Model 1 B+)
	- micro USB power cable (e.g. >=1200 mAh)
	- SD card
	- LAN cable

 Prepare Workspace
 - download raspian wheezy https://www.raspberrypi.org/downloads/
 - download Win32 Diks Imager http://www.softpedia.com/get/CD-DVD-Tools/Data-CD-DVD-Burning/Win32-Disk-Imager.shtml
 - Download SD Card Formatter https://www.sdcard.org/downloads/formatter_4/
 
 Setup Raspberry Pi
 - Insert SD Card in PC
 - open "SD Card Formatter"
 - make sure that your SD card drive is selected and click "Format", confirm
 - Unzip Raspian Wheezy Image and open "Win32 Disk Imager"
 - Select the drive with your SD Card and open the Raspian image
 - Install Raspbian image on SD card by clicking "Write", confirm, wait a few minutes
 
 Configure System
 - insert SD card in raspberry pi and connect power cable, wait for it to boot up
 - select 1 "expand filesystem"
	-- Optional: enable SSH via "Advanced Options" -> "SSH" (for convenience)
	-- Optional: enable Windows Remote Desktop via "sudo apt-get install xrdp"
 - select "Finish", reboot
 - update libraries: "sudo apt-get update"
 
 Install Fritzconnection
 - install dependencies
	-> pip: "sudo apt-get install python-pip", confirm with "y"			
	-> requests "sudo pip install requests"									
	-> libxml and libxslt: "sudo apt-get install libxml2-dev libxslt1-dev"	
	-> sudo apt-get install python2.7-lxml									
 - install fritzconnection: "sudo pip install fritzconnection"		

 

# A FritzBox SpeedMeter using a RaspberryPi and a Blinky Tape
# Pulls Up-/Download speed from Fritzbox and displays it on Blinky Tape. Build for Raspberry Pi Model B.
# Build for Python 2.7.3
# Created by Fabian Utesch with code from BlinkenLabs (https://github.com/Blinkinlabs/BlinkyTape_Python)
# Thanks to Matthew Dyson for inspiration how to use BlinkyTape Code (https://youtu.be/ZEhCh_ezodo)
# Blinky Tape python code and my adaptation is distributet under the MIT license (see LICENSE.md)
# Version 0.1 (2016-05-24)



import serial # to connect to blinky tape
import time   # to connect to blinky tape
import datetime
import glob
from fritzconnection import FritzStatus # to read from FritzBox
# import blinky tape library to connect to blinky tape (https://github.com/Blinkinlabs/BlinkyTape_Python)
# using blinky tape class adapted by Matthew Dyson http://mattdyson.org/blog/2014/01/blinkytape/
from BlinkyTapeV2 import BlinkyTape 

# set default values
length = 60 # Number of LEDs on tape
brightness = 1.0 # (min 0.0 -> max 1.0)
downNow = 0.0
downOld = 0.0
downNew = 0.0
upNow = 0.0
upOld = 0.0
upNew = 0.0
colourR = 0
colourG = 0
colourB = 0
switch = 0
hour = 1

# prepare FritzBox stuff
status = FritzStatus()
(up,down) = status.transmission_rate

# Prepare Blinky Tape stuff
if __name__ == "__main__":

  serialPorts = glob.glob("/dev/ttyACM*")
  port = serialPorts[0]

  bt = BlinkyTape(port)

  # Get max up- and download speed from FritzBox
  (maxUpSpeed,maxDownSpeed) = status.max_bit_rate # gives max up/down speed
  maxUpSpeed = maxUpSpeed/8/1024     # convert to kByte/s
  maxDownSpeed = maxDownSpeed/8/1024 # convert to kByte/s

  print "Start des Speedmeters"
  print("SpeedMeter is running.. (stop with STRG+C)")  # status info

  # get localtime
  localtime = time.asctime(time.localtime(time.time()) )
  hour = time.localtime()[3]

  # indefinitely running code loop
  while(True):

    # update time
    localtime = time.asctime(time.localtime(time.time()) )
    hour = time.localtime()[3]

    # Speed meter is turned off during the night
    if hour>8 and hour<23:
      if switch == 0:
        print localtime, "SpeedMeter display is now ON"
        switch = 1

      # reduce brightness of speed meter in the evening
      if hour > 20 and hour < 7:
        brightness = 0.2
      else:
        brightness = 1.0

      # Get current up- and download speed

      (up,down) = status.transmission_rate # gives downloaded kilobits since last call

      up = up/1024     # convert to kByte/s
      down = down/1024 # convert to kByte/s

      # calculate mean over two seconds to smooth out strange values
      downOld = downNow
      downNow = downNew
      downNew = down

      downMean = (downNew+downNow+downOld)/3
      if downMean > maxDownSpeed:
          downMean = maxDownSpeed
      downPercentMean = float(downMean) / maxDownSpeed

      upOld = upNow
      upNow = upNew
      upNew = up

      upMean = (upNew+upNow+upOld)/3
      if upMean > maxUpSpeed:
          upMean = maxUpSpeed
      upPercentMean = float(upMean) / maxUpSpeed

      #print(downMean,maxDownSpeed) # for debugging

      # smoothing
      downLength = int(downPercentMean*30)
      downRest = downPercentMean*30 - downLength
      upLength = int(upPercentMean*30)
      upRest = upPercentMean*30 - upLength

      # Display speeds   'simple'
      for x in range(length):      
        # Display download speed
          if x < 30:
              if x < downLength:
                  bt.setPixel(x, 0,int(brightness*255),0)  # set color R,G,B
              elif x == downLength:
                  bt.setPixel(x, 0,int(brightness*255*downRest),0)
              else:
                  bt.setPixel(x, 0,0,0)
        # Display upload speed       
          if x > 30:
              if x == (length-upLength):
                  bt.setPixel(x, int(brightness*255*upRest),0,0)
              elif x > (length-upLength): # set color R,G,B
                  bt.setPixel(x, int(brightness*255),0,0)
              else:
                  bt.setPixel(x, 0,0,0)

    else:
      if switch == 1:
        print localtime, "SpeedMeter display is now OFF"
        switch = 0
      for x in range(length):
        bt.setPixel(x, 0,0,0)
        
    bt.sendUpdate() # update BlinkyTape

    time.sleep(1) # wait for 1 second. If used more frequently, FritBox will return 0; don't know why

# known issues
# - no data when Fritz!Box is busy, leads to default rainbow pattern
#   this can be triggered by transfering large data over build in VPN connection
# - Fritz!Box does not answer if queried more frequently than once per second
# - single transmission rates can be faster than maximum download speed. Better
#   smooth over 2 measures.

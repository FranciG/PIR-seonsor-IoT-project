# import libraries
import time 
import os 

while True: # do forever

    

    os.system('fswebcam -r 640x480 -S 10 --jpeg 70  −−set brightness=100%  --save /home/pi/%H%M%S.jpg') # uses Fswebcam to take picture

    time.sleep(15) # delay

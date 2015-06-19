#! /usr/bin/env python

import alsaaudio, audioop, time

if __name__=="__main__":
  #Copypaste from https://stackoverflow.com/questions/1936828/how-get-sound-input-from-microphone-in-python-and-process-it-on-the-fly
  inp=alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)
  inp.setchannels(1)
  inp.setrate(8000)
  inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
  inp.setperiodsize(160)

  while True:
    # Read data from device
    l,data = inp.read()
    if l:
      # Return the maximum of the absolute value of all samples in a fragment.
      print audioop.max(data, 2)
    time.sleep(.001)

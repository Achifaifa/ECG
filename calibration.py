#! /usr/bin/env python

import alsaaudio, audioop, time

if __name__=="__main__":
  #Copypaste from https://stackoverflow.com/questions/1936828/how-get-sound-input-from-microphone-in-python-and-process-it-on-the-fly
  inp=alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)
  inp.setchannels(1)
  inp.setrate(8000)
  inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
  inp.setperiodsize(160)

  minim=10**10
  maxim=-10**10
  while True:
    l,data=inp.read()
    if l: 
      ignore,outd=audioop.minmax(data, 2)
      minim=outd if outd<minim else minim
      maxim=outd if outd>maxim else maxim
      print "\rMAX %i | MIN %i"%(maxim,minim),
    time.sleep(.001)

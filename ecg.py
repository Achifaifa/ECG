#! /usr/bin/env python

import alsaaudio, audioop, time

if __name__=="__main__":
  #Copypaste from https://stackoverflow.com/questions/1936828/how-get-sound-input-from-microphone-in-python-and-process-it-on-the-fly
  inp=alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)
  inp.setchannels(1)
  inp.setrate(8000)
  inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
  inp.setperiodsize(160)

  start=time.time()
  beats=[start]
  previous=0
  while True:
    l,data=inp.read()
    if l:
      outd=audioop.max(data, 2)
      if outd==0 and previous!=0:
        now=time.time()
        bpm=60/(now-beats[-1])
        avg=60*len(beats)/(now-start)
        print "beep (%i BPM; %i AVG) | %i" %(bpm, avg, len(beats))
        beats.append(now)
      previous=outd
    time.sleep(.001)

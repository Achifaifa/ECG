#! /usr/bin/env python

import alsaaudio, audioop, os, time, tkFont, Tkinter
 
# Setup copied from
# stackoverflow.com/questions/1936828/how-get-sound-input-from-microphone-in-python-and-process-it-on-the-fly
inp=alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)
inp.setchannels(1)
inp.setrate(8000)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
inp.setperiodsize(160)
# Count variables
start=time.time()
beats=[start]
previous=0
avg=0
maxim=0
minim=9001
# Chrono window variables
chronorefresh=0
countstarted=0
countdown=[5,0]
chronostime=0
previoustick=time.time()
# Player variables
playername="Stumpy O'Leg McNoleg"
# Create tkinter windows
root=Tkinter.Tk()
root.wm_title("Afraidifier - data")
counter=Tkinter.Toplevel()
counter.wm_title("Afraidifier - chrono")
buttons=Tkinter.Toplevel()
buttons.wm_title("BUTTONS!")
# Define fonts
bigfont=tkFont.Font(root=root, font=None, name=None, family='Sans', size=250, weight='bold')
chronofont=tkFont.Font(root=counter, font=None, name=None, family='Mono', size=250, weight='bold')
smallfont=tkFont.Font(root=root, font=None, name=None, family='Mono', size=75, weight='bold')
# tkinter thing
Tkinter.mainloop(1) 

#Chrono functions
def startf():
  global beats, chronostime, countstarted, start
  print "starting chrono"
  countstarted=1
  beats=beats[-10:]
  start=beats[0]
  chronostime=time.time()

def stopf():
  global countstarted, countdown, playername, avg, maxim, minim, beats
  countstarted=0
  print "stopping chrono"
  try:
    filecounter=0
    while 1:
      if "out_ecg_%s_%03i"%(playername, filecounter) in os.listdir("./"):
        filecounter+=1
      else:
        beatsp=[str(i) for i in beats]
        with open("out_ecg_%s_%03i"%(playername, filecounter),"w+") as outf:
          outf.write("%s\nAVG:%i\nMAX:%i\nMIN:%i\n---\n"%(playername, avg, maxim, minim))
          outf.write("\n".join(beatsp))
        break
    countdown=[5,0]
  except NameError:
    print "No stats generated. Sample list too short"

# Chrono window
name=Tkinter.Label(counter, text=playername, font=smallfont)
name.pack(side="top", padx=10, fill="x")

#Name update
def updatename(namev):
  global name, playername

  try:
    name.pack_forget()
  except NameError:
    pass

  playername=namev
  name=Tkinter.Label(counter, text=playername, font=smallfont)
  name.pack(side="top", padx=10, fill="x")

# Control panel
startbutton=Tkinter.Button(buttons, text="Start", background="#00BB00", foreground="white", command=startf)
stopbutton=Tkinter.Button(buttons, text="Stop", background="#BB0000", foreground="white", command=stopf)
nameform=Tkinter.Entry(buttons)
submitname=Tkinter.Button(buttons, text="update", command=lambda t=nameform.get():updatename(nameform.get()))
nameform.pack()
submitname.pack(fill="x")
startbutton.pack(fill="x")
stopbutton.pack(fill="x")

# Main loop
try:
  while True:
    #Get new audio data
    l,data=inp.read()
    if l:
      try:                  
        z,outd=audioop.minmax(data, 2)
      except audioop.error: 
        outd=0

      # Update chrono widnow
      now=time.time()
      if countstarted:
        if now-previoustick>1:
          countdown[1]-=1
          if countdown[1]==-1:
            countdown[1]=59
            countdown[0]-=1
          previoustick=time.time()

        if not countdown[0] and not countdown[1]:
          stopf()
      
      try:    
        timeleft.pack_forget()
      except NameError: 
        pass
      timeleft=Tkinter.Label(counter, text="%02i:%02i"%(countdown[0],countdown[1]), font=chronofont)
      timeleft.pack()

      if chronorefresh%100<5: counter.update()

      # If the amplitude has reached a limit
      if outd>3000 and previous<3000:
        now=time.time()
        # Calculate current BPM
        try:                
          bpm=300/(now-beats[-5])
        except IndexError:  
          bpm=0
        # Calculate total average
        avg=60*len(beats)/(now-start)
        beats.append(now)
        # Calculate maximums
        if len(beats)>5:
          maxim=bpm if bpm>maxim else maxim
          minim=bpm if bpm<minim else minim
        # Update TKinter windows
        try: 
          beatslabel.pack_forget()
          statslabel.pack_forget()
          spacer.pack_forget()
        except NameError:
          pass

        if bpm<20:
          beatslabel=Tkinter.Label(root, text="---", font=bigfont)
        else:
          beatslabel=Tkinter.Label(root, text=int("%03i"%bpm), font=bigfont)
        beatslabel.pack()

        spacer=Tkinter.Label(root, text="\n\n\n")
        spacer.pack()

        if len(beats)<10:
          statslabel=Tkinter.Label(root, text=" MIN | AVG | MAX \n--- | --- | ---", font=smallfont)
        else:
          statslabel=Tkinter.Label(root, text=" MIN | AVG | MAX \n%03i | %03i | %03i"%(minim,avg,maxim), font=smallfont)
        statslabel.pack()

        # Update root window
        root.update()
      #save previous max amplitude
      previous=outd
    chronorefresh+=1
    time.sleep(.001)

# Display stats and save beat list to file
except (KeyboardInterrupt, Tkinter.TclError):
  print "\rProgram ended"

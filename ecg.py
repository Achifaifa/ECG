#! /usr/bin/env python

import alsaaudio, audioop, os, time, tkFont, Tkinter
 
if __name__=="__main__":
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
  maxim=0
  minim=9001
  # Chrono window variables
  chronorefresh=0
  countstarted=0
  countdown=[5,0]
  # Create tkinter windows
  root=Tkinter.Tk()
  root.wm_title("Afraidifier - data")
  counter=Tkinter.Toplevel()
  counter.wm_title("Afraidifier - chrono")
  # Define fonts
  bigfont=tkFont.Font(root=root, font=None, name=None, family='Sans', size=250, weight='bold')
  chronofont=tkFont.Font(root=counter, font=None, name=None, family='Mono', size=180, weight='bold')
  smallfont=tkFont.Font(root=root, font=None, name=None, family='Mono', size=75, weight='bold')
  # tkinter thing
  Tkinter.mainloop(1) 
  # Main loop
  try:
    while True:
      #Get new audio data
      l,data=inp.read()
      if l:
        try:
          ignore,outd=audioop.minmax(data, 2)
        except audioop.error: 
          outd=0

        # Update chrono widnow
        now=time.time()
        try:
          timeleft.pack_forget()
          startbutton.pack_forget()
          stopbutton.pack_forget()
        except:
          pass
        startbutton=Tkinter.Button(counter, text="Start", height=10, width=30, background="#00BB00", foreground="white")
        stopbutton=Tkinter.Button(counter, text="Stop", height=10, width=30, background="#BB0000", foreground="white")
        timeleft=Tkinter.Label(counter, text="%02i:%02i"%(countdown[0],countdown[1]), font=chronofont)
        timeleft.pack()
        startbutton.pack(side="left", padx=10, expand=True)
        stopbutton.pack(side="right", padx=10, expand=True)
        if chronorefresh%100==0:
          counter.update_idletasks()

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
            title.pack_forget()
            title2.pack_forget()
            title3.pack_forget()
          except:
            pass
          if bpm<20:
            title=Tkinter.Label(root, text="---", font=bigfont)
          else:
            title=Tkinter.Label(root, text=int("%03i"%bpm), font=bigfont)
          title.pack()
          title3=Tkinter.Label(root, text="\n\n\n")
          title3.pack()
          if len(beats)<10:
            title2=Tkinter.Label(root, text=" MIN | AVG | MAX \n--- | --- | ---", font=smallfont)
          else:
            title2=Tkinter.Label(root, text=" MIN | AVG | MAX \n%03i | %03i | %03i"%(minim,avg,maxim), font=smallfont)
          title2.pack()
          # Update root window
          root.update()
        #save previous max amplitude
        previous=outd
      chronorefresh+=1
      time.sleep(.001)

  # Display stats and save beat list to file
  except (KeyboardInterrupt, Tkinter.TclError):
    try:
      print "Program ended"
      print "MAX: %03i\nMIN: %03i\nAVG: %03i"%(maxim,minim,avg)
      filecounter=1
      # while 1:
      #   if "out_ecg_%03i"%filecounter in os.listdir("./"):
      #     filecounter+=1
      #   else:
      #     beats=[str(i) for i in beats]
      #     with open("out_ecg_%03i"%filecounter,"w+") as outf:
      #       outf.write("\n".join(beats))
      #     break
    except NameError:
      print "No stats generated. Sample list too short"

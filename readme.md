#ECG

Software to record ECG data from a cardiac monitor. The monitor (Bexen bexkop) is plugged into the computer via microphone (The machine sends voltage spikes during QRS) using a ECG compatible plug in the back of the machine.

* Calibration.py
Run this with the machine connected. Logs the maximum and minimum values of the sound amplitude. 

Adjust your microphone gain until the maximum reads between 3500 and 4000. It will be low enough not to hear much, but it probably avoids damage to the computer. The minimum does nothing but, just in case, it should read almost exactly the opposite.

* ecg.py
This program reads the signals from the machine and calculates current BPM, maximum, minimum and total average, and displays the information in a tkinter based window. 

In another window shows the current user name and a countdown. When the countdown reaches zero, all the data (Name, stats, etc) is written to a text file.

A third pop-up window contains the control buttons. "Start" starts the countdown, "Stop" resets the countdown and writes the data to file, and "Update" places the name in the form in the countdown screen

#ECG

Software to record ECG data from a cardiac monitor. The monitor (Bexen bexkop) is plugged into the computer via microphone (The machine sends voltage spikes during QRS) using a ECG compatible plug in the back of the machine.

* Calibration.py
Run this with the machine connected. Logs the maximum and minimum values of the sound amplitude. 

Adjust your microphone gain until the maximum reads between 3500 and 4000. It will be low enough not to hear much, but it probably avoids damage to the computer. The minimum does nothing but, just in case, it should read almost exactly the opposite.

* ecg.py
This program reads the signals from the machine and calculates current BPM, maximum, minimum and total average. 

It displays the information in a tkinter based window. Once it's done it displays maximum, minimum and average and writes a file to disk containing the timestamp of every heartbeat registered so stats can be generated later.

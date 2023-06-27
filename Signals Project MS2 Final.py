import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append(r'c:\users\dell\appdata\local\packages\pythonsoftwarefoundation.python.3.9_qbz5n2kfra8p0\localcache\local-packages\python39\site-packages')
import sounddevice as sd
from scipy import pi
from scipy.fftpack import fft 

a = 12*1024
t=np.linspace(0,3,a) #creates array for time between 0 and 3 with num of elements 12288

def piano(start, end, freq):
       unitStep=np.heaviside(t-start,1)
       unitStepShift=np.heaviside(t-end,1)
       difference=unitStep-unitStepShift
       v=np.sin(freq*2*(np.pi)*t)
       x=np.multiply(v,difference)
       return x
   
#THIS TONE IS F4 FROM t=0 TO t=0.3
x1 = piano (0,0.3,349.23) 

#THIS TONE IS A4 FROM t=0.3 TO t=0.6
x2 = piano (0.3,0.6,440) 

#THIS TONE IS F4 FROM t=0.6 TO t=0.9
x3 = piano (0.6 ,0.9,349.23) 

#THIS TONE IS E4 FROM t= 0.9 TO 1.5
x4 = piano (0.9,1.5,329.63)

#THIS TONE IS F4 FROM t= 1.5 TO 1.8
x5 = piano (1.6, 1.8,349.23 )

#THIS TONE IS A4 FROM t= 1.8 TO 2.1
x6 = piano (1.8,2.1,440)

#THIS TONE IS E4 FROM t= 2.1 TO 2.4
x7 = piano (2.1,2.4,329.63)

#THIS TONE IS D4 FROM t= 2.4 TO 3
x8 = piano (2.4,3, 293.66)

summation = x1+x2+x3+x4+x5+x6+x7+x8

#FREQUENCY DOMAIN FOR THE ORIGINAL SONG
N = 3*1024
frequency = np.linspace (0.0, 512, int(N/2)) 
summation_f = fft(summation)
y_amplitude = 2/N * np.abs (summation_f [0: int(N/2)])

#Generating noise and adding it to the song
f1,f2 = np.random.randint(0, 512, 2)
n = np.sin(2*f1*np.pi*t) + np.sin(2*f2*np.pi*t) #NOISE
addnoise = summation + n
print (f1,f2)

#FREQUENCY DOMAIN FOR THE ADDNOISE
addnoise_f = fft(addnoise)
addnoise_amplitude = 2/N * np.abs (addnoise_f [0: int(N/2)])

i = 0
max1 = 0
max2 = 0
maxindex1 = -1
maxindex2 = -1
length = len(addnoise_amplitude)
while (i<length-1):
    if (addnoise_amplitude[i] > max1):
        max2 = max1
        maxindex2 = maxindex1
        max1 = addnoise_amplitude[i]
        maxindex1 = i
    elif (addnoise_amplitude[i] > max2):
        max2 = addnoise_amplitude[i]
        maxindex2 = i
    i = i + 1
print (maxindex1,maxindex2)

#Getting both max frequencies 
y1 = int(frequency[maxindex1])
y2 = int(frequency[maxindex2])
print (y1,y2)

#Removing the noise from the song
xFiltered= addnoise - (np.sin(2*y1*np.pi*t) + np.sin(2*y2*np.pi*t)) 

#Frequency Domain of xFiltered
xFiltered_f= fft(xFiltered)
xFiltered_amplitude = 2/N * np.abs (xFiltered_f [0: int(N/2)])

plt.plot(t, addnoise)
plt.title ('Time Domain With Noise')
plt.xlabel ('Time')
plt.ylabel('Amplitude')
plt.show()

plt.plot(frequency, addnoise_amplitude)
plt.title('Frequency Domain Signal With Noise')
plt.xlabel('Frequency in Hz')
plt.ylabel('Amplitude')
plt.show()

plt.plot(t, xFiltered)
plt.title('Time Domain Signal xFiltered')
plt.xlabel('Frequency in Hz')
plt.ylabel('Amplitude')
plt.show()

plt.plot(frequency, xFiltered_amplitude)
plt.title('Frequency Domain Signal xFiltered')
plt.xlabel('Frequency in Hz')
plt.ylabel('Amplitude')
plt.show()

sd.play(xFiltered,N)
#sd.play(summation,N)




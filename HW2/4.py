import csv
import numpy as np
import matplotlib.pyplot as plt

#import data
t_a = [] # column 0
data_a = [] # column 1
with open('sigA.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        t_a.append(float(row[0])) # leftmost column
        data_a.append(float(row[1])) # second column
t_b = [] # column 0
data_b = [] # column 1
with open('sigB.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        t_b.append(float(row[0])) # leftmost column
        data_b.append(float(row[1])) # second column
t_c = [] # column 0
data_c = [] # column 1
with open('sigC.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        t_c.append(float(row[0])) # leftmost column
        data_c.append(float(row[1])) # second column
t_d = [] # column 0
data_d = [] # column 1
with open('sigD.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        t_d.append(float(row[0])) # leftmost column
        data_d.append(float(row[1])) # second column

#Fourier Transform
Fs_a = len(t_a)/t_a[-1]
Fs_b = len(t_b)/t_b[-1]
Fs_c = len(t_c)/t_c[-1]
Fs_d = len(t_d)/t_d[-1]
Ts_a = 1.0/Fs_a
Ts_b = 1.0/Fs_a
Ts_c = 1.0/Fs_c
Ts_d = 1.0/Fs_d
ts_a = np.arange(0,t_a[-1],Ts_a)
ts_b = np.arange(0,t_b[-1],Ts_b)
ts_c = np.arange(0,t_c[-1],Ts_c)
ts_d = np.arange(0,t_d[-1],Ts_d)
k_a = np.arange(len(data_a))
k_b = np.arange(len(data_b))
k_c = np.arange(len(data_c))
k_d = np.arange(len(data_d))
T_a = len(data_a)/Fs_a
T_b = len(data_b)/Fs_b
T_c = len(data_c)/Fs_c
T_d = len(data_d)/Fs_d
frq_a = (k_a/T_a)[range(int(len(data_a)/2))]
frq_b = (k_b/T_b)[range(int(len(data_b)/2))]
frq_c = (k_c/T_c)[range(int(len(data_c)/2))]
frq_d = (k_d/T_d)[range(int(len(data_d)/2))]
Y_a = (np.fft.fft(data_a)/len(data_a))[range(int(len(data_a)/2))]
Y_b = (np.fft.fft(data_b)/len(data_b))[range(int(len(data_b)/2))]
Y_c = (np.fft.fft(data_c)/len(data_c))[range(int(len(data_c)/2))]
Y_d = (np.fft.fft(data_d)/len(data_d))[range(int(len(data_d)/2))]

fig, (a1, a2) = plt.subplots(2, 1)
a1.set_title('Signal A')
a1.plot(t_a,data_a,'b')
a1.set_xlabel('Time')
a1.set_ylabel('Amplitude')
a2.set_title('FFT')
a2.loglog(frq_a,abs(Y_a),'b') # plotting the fft
a2.set_xlabel('Freq (Hz)')
a2.set_ylabel('|Y(freq)|')
plt.show()

fig1, (b1, b2) = plt.subplots(2, 1)
b1.set_title('Signal B')
b1.plot(t_b,data_b,'b')
b1.set_xlabel('Time')
b1.set_ylabel('Amplitude')
b2.set_title('FFT')
b2.loglog(frq_b,abs(Y_b),'b') # plotting the fft
b2.set_xlabel('Freq (Hz)')
b2.set_ylabel('|Y(freq)|')
plt.show()

fig2, (c1, c2) = plt.subplots(2, 1)
c1.set_title('Signal C')
c1.plot(t_c,data_c,'b')
c1.set_xlabel('Time')
c1.set_ylabel('Amplitude')
c2.set_title('FFT')
c2.loglog(frq_c,abs(Y_c),'b') # plotting the fft
c2.set_xlabel('Freq (Hz)')
c2.set_ylabel('|Y(freq)|')
plt.show()

fig3, (d1, d2) = plt.subplots(2, 1)
d1.set_title('Signal D')
d1.plot(t_d,data_d,'b')
d1.set_xlabel('Time')
d1.set_ylabel('Amplitude')
d2.set_title('FFT')
d2.loglog(frq_d,abs(Y_d),'b') # plotting the fft
d2.set_xlabel('Freq (Hz)')
d2.set_ylabel('|Y(freq)|')
plt.show()
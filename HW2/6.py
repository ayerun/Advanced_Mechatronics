import csv
import numpy as np
import matplotlib.pyplot as plt

#average data points
def weighted_average(A,data):
    avg = []
    B = (1-A)
    for i in range(len(data)):
        if i == 0:
            avg.append(B*data[i])
        else:
            avg.append(A*avg[i-1]+B*data[i])
    return avg

#perform fft
def my_fft(data,t):
    Fs = len(t)/t[-1]
    Ts = 1.0/Fs
    ts = np.arange(0,t[-1],Ts)
    k = np.arange(len(data))
    T = len(data)/Fs
    frq = (k/T)[range(int(len(data)/2))]
    Y = (np.fft.fft(data)/len(data))[range(int(len(data)/2))]
    return frq,Y

def import_data(filename):
    t = []
    data = []
    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            t.append(float(row[0]))
            data.append(float(row[1]))
    return t,data


#import data
t_a,data_a = import_data('sigA.csv')
t_b,data_b = import_data('sigB.csv')
t_c,data_c = import_data('sigC.csv')
t_d,data_d = import_data('sigD.csv')

#weights
A_a = 0.9965
A_b = 0.993
A_c = 0.5
A_d = 0.9

#average points
data_fa = weighted_average(A_a,data_a)
data_fb = weighted_average(A_b,data_b)
data_fc = weighted_average(A_c,data_c)
data_fd = weighted_average(A_d,data_d)

#fourier transform
frq_fa, Y_fa = my_fft(data_fa,t_a)
frq_a, Y_a = my_fft(data_a,t_a)
frq_fb, Y_fb = my_fft(data_fb,t_b)
frq_b, Y_b = my_fft(data_b,t_b)
frq_fc, Y_fc = my_fft(data_fc,t_c)
frq_c, Y_c = my_fft(data_c,t_c)
frq_fd, Y_fd = my_fft(data_fd,t_d)
frq_d, Y_d = my_fft(data_d,t_d)

#plot
plt.figure(0)
plt.loglog(frq_a,abs(Y_a),'k')
plt.loglog(frq_fa,abs(Y_fa),'r')
plt.xlabel('Freq (Hz)')
plt.ylabel('|Y(freq)|')
plt.title("FFT of Signal A: A = {:3f}, B = {:3f}".format(A_a,1-A_a))
plt.legend(['unfiltered','filtered'])
plt.show()
plt.figure(1)
plt.loglog(frq_b,abs(Y_b),'k')
plt.loglog(frq_fb,abs(Y_fb),'r')
plt.xlabel('Freq (Hz)')
plt.ylabel('|Y(freq)|')
plt.title("FFT of Signal B: A = {:3f}, B = {:3f}".format(A_b,1-A_b))
plt.legend(['unfiltered','filtered'])
plt.show()
plt.figure(2)
plt.loglog(frq_c,abs(Y_c),'k')
plt.loglog(frq_fc,abs(Y_fc),'r')
plt.xlabel('Freq (Hz)')
plt.ylabel('|Y(freq)|')
plt.title("FFT of Signal C: A = {:3f}, B = {:3f}".format(A_c,1-A_c))
plt.legend(['unfiltered','filtered'])
plt.show()
plt.figure(3)
plt.loglog(frq_d,abs(Y_d),'k')
plt.loglog(frq_fd,abs(Y_fd),'r')
plt.xlabel('Freq (Hz)')
plt.ylabel('|Y(freq)|')
plt.title("FFT of Signal D: A = {:3f}, B = {:3f}".format(A_d,1-A_d))
plt.legend(['unfiltered','filtered'])
plt.show()


#plot signal
# plt.plot(t_c,data_c,'r')
# plt.plot(t_c,data_fc,'k')
# plt.xlabel('Time [s]')
# plt.ylabel('Signal')
# plt.title('Signal C')
# plt.show()
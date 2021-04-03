import csv
import numpy as np
import matplotlib.pyplot as plt

#average data points
def moving_average(X,data,t):
    count = 0
    avg = 0
    avg_t = 0
    data_fa = []
    t_fa = []
    for i in range(len(data)):
        avg += data[i]
        avg_t += t[i]
        count += 1
        if count == X:
            avg = avg/count
            avg_t = avg_t/count
            data_fa.append(avg)
            t_fa.append(avg_t)
            avg = 0
            avg_t = 0
            count = 0
        elif i == len(data_a):
            avg = avg/count
            avg_t = avg_t/count
            data_fa.append(avg)
            t_fa.append(avg_t)
            avg = 0
            avg_t = 0
            count = 0
    return data_fa,t_fa

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

#number of points to average
X_a = 300
X_b = 50
X_c = 10
X_d = 25

#average points
data_fa, t_fa = moving_average(X_a,data_a,t_a)
data_fb, t_fb = moving_average(X_b,data_b,t_b)
data_fc, t_fc = moving_average(X_c,data_c,t_c)
data_fd, t_fd = moving_average(X_d,data_d,t_d)

#fourier transform
frq_fa, Y_fa = my_fft(data_fa,t_fa)
frq_a, Y_a = my_fft(data_a,t_a)
frq_fb, Y_fb = my_fft(data_fb,t_fb)
frq_b, Y_b = my_fft(data_b,t_b)
frq_fc, Y_fc = my_fft(data_fc,t_fc)
frq_c, Y_c = my_fft(data_c,t_c)
frq_fd, Y_fd = my_fft(data_fd,t_fd)
frq_d, Y_d = my_fft(data_d,t_d)

#plot
plt.figure(0)
plt.loglog(frq_a,abs(Y_a),'r')
plt.loglog(frq_fa,abs(Y_fa),'k')
plt.xlabel('Freq (Hz)')
plt.ylabel('|Y(freq)|')
plt.title("FFT of Signal A: X = {:d}".format(X_a))
plt.show()
plt.figure(1)
plt.loglog(frq_b,abs(Y_b),'r')
plt.loglog(frq_fb,abs(Y_fb),'k')
plt.xlabel('Freq (Hz)')
plt.ylabel('|Y(freq)|')
plt.title("FFT of Signal B: X = {:d}".format(X_b))
plt.show()
plt.figure(2)
plt.loglog(frq_c,abs(Y_c),'r')
plt.loglog(frq_fc,abs(Y_fc),'k')
plt.xlabel('Freq (Hz)')
plt.ylabel('|Y(freq)|')
plt.title("FFT of Signal C: X = {:d}".format(X_c))
plt.show()
plt.figure(3)
plt.loglog(frq_d,abs(Y_d),'r')
plt.loglog(frq_fd,abs(Y_fd),'k')
plt.xlabel('Freq (Hz)')
plt.ylabel('|Y(freq)|')
plt.title("FFT of Signal D: X = {:d}".format(X_d))
plt.show()


#plot signal
# plt.plot(t_d,data_d,'r')
# plt.plot(t_fd,data_fd,'k')
# plt.xlabel('Time [s]')
# plt.ylabel('Signal')
# plt.title('Signal D')
# plt.show()
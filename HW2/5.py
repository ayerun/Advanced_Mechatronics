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
            data_fa.append(avg)
            t_fa.append(avg_t)
            avg = 0
            avg_t = 0
            count = 0
        elif i == len(data_a):
            avg = avg/count
            data_fa.append(avg)
            t_fa.append(avg_t)
            avg = 0
            avg_t = 0
            count = 0
    return data_fa,t_fa

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

#number of points to average
X_a = 10
X_b = 10
X_c = 10
X_d = 10


# count = 0
# avg = 0
# avg_t = 0
# data_fa = []
# t_fa = []
# for i in range(len(data_a)):
#     avg += data_a[i]
#     avg_t += t_a[i]
#     count += 1
#     if count == X_a:
#         avg = avg/count
#         data_fa.append(avg)
#         t_fa.append(avg_t)
#         avg = 0
#         avg_t = 0
#         count = 0
#     elif i == len(data_a):
#         avg = avg/count
#         data_fa.append(avg)
#         t_fa.append(avg_t)
#         avg = 0
#         avg_t = 0
#         count = 0
data_fa, t_fa = moving_average(X_a,data_a,t_a)
print(len(data_fa))
print(len(data_a))


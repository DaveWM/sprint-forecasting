import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib.ticker as ticker
import numpy as np
import scipy.stats as stats
import math
import datetime

days_in_sprint = 14

def intInput():
    x = input()
    return int(x)

print("Start date (dd/MM/yyyy):")
date_string = input()
d, m, y = map(int, date_string.split('/'))
start_date = datetime.date(y,m,d)
print("Number of stories low guess:")
nl = intInput()
print("Number of stories high guess:")
nh = intInput()
print("Split factor low guess:")
sl = intInput()
print("Split factor high guess:")
sh = intInput()
print("Throughput low guess:")
tl = intInput()
print("Throughput high guess:")
th = intInput()

def calc(high, low):
    mean = (high + low) / 2
    sd = ((high - low) / 4) ** 0.5
    return mean, sd

n, n_err = calc(nh, nl)
s, s_err = calc(sh, sl)
t, t_err = calc(th, tl)

time = (n * s) / t
time_err = time * (((n_err/n) ** 2 + (s_err/s) ** 2 + (t_err/t) ** 2) ** 0.5)

def to_date(num_sprints):
    delta = datetime.timedelta(days = (num_sprints * days_in_sprint))
    return start_date + delta

def date_to_string(d):
    return d.strftime("%d/%m/%y")

def format_time(num_sprints):
    return date_to_string(to_date(num_sprints))

print(f"\n\nEstimated completion date is {format_time(time)} +/- {time_err * days_in_sprint:.2f} days")
print(f"95%: {format_time(time + 2 * time_err)}")
print(f"68%: {format_time(time + time_err)}")
print(f"50%: {format_time(time)}")
print(f"32%: {format_time(time - time_err)}")
print(f"5%: {format_time(time - 2 * time_err)}")

@ticker.FuncFormatter
def tick_formatter(x, pos):
    return format_time(x)

def plot(mu, sigma):
    x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
    fig, ax = plt.subplots()
    ax.plot(x, stats.norm.pdf(x, mu, sigma), '-o', markevery=[5, 32, 50, 68, 95])
    ax.xaxis.set_major_formatter(tick_formatter)
    plt.show()

plot(time, time_err)
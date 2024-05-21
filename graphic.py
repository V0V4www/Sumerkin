import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
import math

with open("/home/b04-306/Sumerkin/settings.txt", "r") as file_1:
    li = file_1.read().split("\n")
    settings_data = [float(num) for num in li]

data_arr = np.loadtxt("/home/b04-306/Sumerkin/data.txt", dtype=int)

volt_step = settings_data[1]
time_step = settings_data[0]

volt_arr = data_arr * volt_step
time_arr = np.arange(0, len(data_arr)) * time_step

volt_max     = np.max(volt_arr)
volt_max_ind = np.argmax(volt_arr)
time_max     = np.max(time_arr)
time_max_ind = np.argmax(time_arr)

charge_data = [time_arr[0:volt_max_ind:], volt_arr[0:volt_max_ind:]]
discharge_data = [time_arr[volt_max_ind::], volt_arr[volt_max_ind::]]

figure, axes = plt.subplots(figsize = (16, 10), dpi = 400)

axes.set_xlabel("Time, sec", fontsize = 16)
axes.set_ylabel("Voltage, V", fontsize = 16)
axes.set_title("RC circuit", fontsize = 20)

charge_plot_line   , = axes.plot(charge_data[0], charge_data[1], linewidth=4, color ='r', alpha=0.6)
discharge_plot_line, = axes.plot(discharge_data[0], discharge_data[1], linewidth=4, color ='blue', alpha=0.6)

axes.plot(charge_data[0][::20], charge_data[1][::20], linestyle=None, color ='r', markersize=10, marker='o')
axes.plot(discharge_data[0][::20], discharge_data[1][::20], linestyle=None, color ='blue', markersize=10, marker='o')


charge_plot_line.set_label("Capacitor charges")
discharge_plot_line.set_label("Capacitor discharges")
axes.legend()

x_lim = (0.0, math.ceil(time_max))
y_lim = (0.0, 3.0)
axes.set(xlim = x_lim, ylim = y_lim)

axes.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
axes.xaxis.set_major_locator(ticker.MultipleLocator(1.0))
axes.yaxis.set_minor_locator(ticker.MultipleLocator(0.125))
axes.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
axes.grid(color = "grey", which = "minor", linestyle = '-.', linewidth = 0.75)
axes.grid(color = "grey", which = "major", linestyle = '-', linewidth = 1)

charge_time    = time_arr[volt_max_ind] - time_arr[0]
discharge_time = time_arr[-1] - time_arr[volt_max_ind]

axes.text(x = (charge_time/2), y = volt_max/2, s = ("Charge time: " + str(round(charge_time, 2)) + " sec"), color = 'red', fontsize = 14)
axes.text(x = (charge_time+discharge_time/2), y = volt_max/2, s = ("Discharge time: " + str(round(discharge_time, 2)) + " sec"), color = 'blue', fontsize = 14)

plt.plot()
figure.savefig("/home/b04-306/Sumerkin/graphic.svg")

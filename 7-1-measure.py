import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import time
  # настроить GPIO на Raspberry Pi
#GPIO.cleanup()
comp = 14
dac = [8, 11, 7, 1, 0, 5, 12, 6]
led = [2, 3, 4, 17, 27, 22, 10, 9]
troyka = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = 1)
GPIO.setup(comp, GPIO.IN)

def dec2bin(num):
    return [int(i) for i in bin(num)[2:].zfill(8)]

  # добавить в скрипт функцию, измеряющую напряжение на выходе тройка-модуля
def adc():
    signal = [0] * 8
    for i in range(8):
        signal[i] = 1
        GPIO.output(dac, signal)
        time.sleep(0.004)
        value = int(''.join([str(i) for i in signal]), 2)
        voltage = value / 256 * 3.3
        comparatorValue = GPIO.input(comp)
        if comparatorValue == 1:
            signal[i] = 0
    True_value = int(''.join([str(i) for i in signal]), 2)
   
    return True_value
    
    return True_value
  # добавить в скрипт функцию, выводящую двоичное представление числа в область светодиодов
def show_(num):
    li = dec2bin(num)
    GPIO.output(dac, li)
    GPIO.output(led, li)
    return li
  # разместить "исполняемую" часть скрипта в блоке try
try:
    voltage_data = []  # создать пустой список для добавления новых измерений
    val = 0  
    GPIO.output(troyka, 1)  # подать напряжение 3.3В на вход тройка-модуля
    time_start = time.time()  # сохранить в переменную момент начала измерений
   
    while(val < 203):  # Провести измерения во время заряда конденсатора
        val = adc()  # измерять напряжение на выходе тройка-модуля и добавлять новые измерения в список
        voltage_data.append(val/ 256 * 3.3)
        print(val)
        show_(val)
        
    GPIO.output(troyka, 0)  # подать напряжение 0.0В на вход тройка-модуля
    while (val > 170):  # перейти к следующей части эксперимента после того, как выходное напряжение RC-цепи достигнет 97% от входного
        print(val)
        val = adc()
        show_(val)
        voltage_data.append(val / 256 * 3.3)
    # перейти к следующей части эксперимента после того, как выходное напряжение RC-цепи достигнет 2% от входного напряжения
    time_fin = time.time()  # сохранить в переменную момент завершения измерений
    exp_span = time_fin - time_start  # определить продолжительность эксперимента
    time = []

    for i in range(0, len(voltage_data)):
        q = exp_span / len(voltage_data)
        time.append(i * q)
    volts = [str(i) for i in voltage_data]
    with open("data.txt", "w") as file:  # сохранить в текстовый файл data.txt показания АЦП, записанные в столбик
        file.write("\n".join(volts))
    with open("settings.txt", "w") as file:  # сохранить в текстовый файл settings.txt среднюю частоту дискретизации проведённых измерений и шаг квантования АЦП
        file.write(str(len(voltage_data)/exp_span))
        file.write("\n")
        file.write(str(3.3/256))

    plt.plot(time, voltage_data, linestyle='-.')
    #plt.savefig("graphic.png")
    plt.show()  # построить график зависимости показаний АЦП от номера измерения
    #print(time_fin)
    #print(time_start)
    print(f'span of experiment: {round(exp_span, 1)} sec')
    print(f'period of 1 measurement: {round(exp_span/len(voltage_data), 3)} sec')
    print(f'average discretization frequency: {int(len(voltage_data)/exp_span)} Hz')
    print(f'ADC: {round(3.3/256, 3)} V')
    #print(voltage_data)
    #print(time)
    
finally:  # подать 0 на все GPIO выходы и сбросить настройки GPIO в блоке finally
    GPIO.output(led, GPIO.LOW)
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup()
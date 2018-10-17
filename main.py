import ntptime
import esp
import machine
from time import sleep, localtime
from machine import Pin, Timer

TIMEZONE = 2
RESYNC = 7200 # Resync once in two hours
countdown = 0 # NTP
countsecond = 0 # TIME

clock = Pin(15, Pin.OUT)  #shcp
latch = Pin(14, Pin.OUT)  #stcp storage register
data = Pin(13, Pin.OUT)  #DS 

def bin2bcd(v):
    return v + 6 * (v // 10)
    #return (v // 10 * 16) + (v % 10)

def shiftOut(byte):
    latch.off()
    for i in range(8):
            value = byte & 128>>i
            data.value(value)
            clock.on()
            clock.off()

sleep_time = 0.00001

def dump_time(time):
    shiftOut(bin2bcd(time))
    latch.on()
    sleep(sleep_time)

def dump(hour, minute, second):
    global countsecond
    if countsecond <= 0 :
        dump_time(hour)
        dump_time(minute)
        countsecond = 1
    if second == 0:
        dump_time(hour)
        dump_time(minute)

def run():
    global countdown
    if countdown <= 0:
        ntptime.settime()
        countdown = RESYNC
    countdown -= 1
    print(countdown)
    year, month, day, hour, minute, second, _, millis = localtime()
    dump((hour + TIMEZONE) % 24, minute, second)
    print("Time (ESP) is %02d:%02d:%02d" % ((hour + TIMEZONE) %24, minute, second))
    sleep(1)

while True:
    run()


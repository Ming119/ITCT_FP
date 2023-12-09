
# 從 gpiozero 模組當中載入 LED 功能
from gpiozero import LED
from time import sleep
import time, sys, math
from grove.adc import ADC
from hamming_code import hamming_decode, hamming_encode
led = LED(13)
__all__ = ["GroveLightSensor"]
# led = LED("GPIO27")   # 給 GPIO 腳位，跟上一行意義相同！
# led = LED("J8:13")    # 定義為樹莓派的腳位

signal = 0
def led_light(msg):
  print()
  global signal
  signal = 0
  for i in msg:
    #print('bit {}'.format(i))
    if i == '1':
      led.on()
    else:
      led.off()
    sleep(0.003)
    signal = 1
    while signal == 1:
      pass


def read_light(channel, threshold):
  global signal
  adc = ADC()
  value = 0
  c = 0
  m = ''
  while True:
    value += adc.read(channel)
    c += 1
    if signal == 1:
      if value / c > threshold:
        m += '1'
      else:
        m += '0'
      signal = 0
      value = 0
      c = 0
      if len(m) == 12:
        print(hamming_decode(m),end = '')
        m = ''

def send_msg(msg):
  thread2 = threading.Thread(target=led_light,args = [msg,])
  thread2.start()
  thread2.join()
from grove.helper import SlotHelper
import threading
sh = SlotHelper(SlotHelper.ADC)
pin = sh.argv2pin()
thread1 = threading.Thread(target=read_light,args = [pin,400,]).start()
#1010 1010 170
#0111 0110 166
msg = hamming_encode('hellow\n')
print(msg)
msg = msg[0] + '0' + msg[2:]
print(msg)
send_msg(msg)

msg = hamming_encode('word\n')
print(msg)
msg = msg[0] + '1' + msg[2:]
print(msg)
send_msg(msg)






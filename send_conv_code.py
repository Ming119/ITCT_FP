
# 從 gpiozero 模組當中載入 LED 功能
from gpiozero import LED
from time import sleep, time
import  sys, math
from grove.adc import ADC
from hamming_code import hamming_decode, hamming_encode
import conv_code
from bitarray import bitarray
led = LED(13)
__all__ = ["GroveLightSensor"]
# led = LED("GPIO27")   # 給 GPIO 腳位，跟上一行意義相同！
# led = LED("J8:13")    # 定義為樹莓派的腳位
# 0  for start sensing a bit
# 1  for end sensing a bit
# -1 for do not thing
signal = -1 
def led_light(msg):
  print()
  global signal
  signal = 0
  for i in msg:
    if i == '1':
      led.on()
    else:
      led.off()
    sleep(0.005)
    signal = 1
    while signal == 1:
      pass
  signal = -1



def read_light_conv(channel, threshold):
  global signal
  flag = False
  adc = ADC()
  value = 0
  c = 0
  m = ''
  while True:
    if signal == 0:
      value += adc.read(channel)
      c += 1
    elif signal == 1:
      if value / c > threshold:
        m += '1'
      else:
        m += '0'
      signal = 0
      value = 0
      c = 0
      flag = True
    else:
      if flag:
        d_code, corrected_errors = conv_code.decoder(m)
        msg_l = []
        for i in range(len(d_code) // 8):   # convert from binary-sring value to integer
            val = "".join(d_code[i * 8:i * 8 + 8])
            msg_l.append(int(val, 2))
        #print(msg_l)
        print('output: ' + bytes(msg_l).decode("utf-8"))   # finally decode to a regular string
        print('corrected errors {}'.format(corrected_errors))
        flag = False
        m = ''
      else:
        pass

def send_msg(msg):
  thread2 = threading.Thread(target=led_light,args = [msg,])
  thread2.start()
  thread2.join()

from grove.helper import SlotHelper
import threading
sh = SlotHelper(SlotHelper.ADC)
pin = sh.argv2pin()





#test conv code
thread1 = threading.Thread(target=read_light_conv,args = [pin,400,]).start()

msg_b = 'hello'.encode("utf-8")
bit_seq = ''
for byte in msg_b:  # get bytes to binary values; every bits store to sublist
    bit_seq +=  f"{byte:08b}"
#conv encode
code = conv_code.encoder(bit_seq)
print('code before transmission: {}'.format(code))
import random
code_ = bitarray(code)
for _ in range(5):
    idx = random.randint(0, len(code) - 1)
    code_[idx] = not (code_[idx])
code_ = str(code_)[10:-2]
print('code after  transmission: {}'.format(code_))
print('before transmission == after transmission: {}'.format(code == code_))
send_msg(code_)

print('wait 2 sec')
start = time()
while time() - start < 2:
  pass
print()
msg_b = 'word'.encode("utf-8")
bit_seq = ''
for byte in msg_b:  # get bytes to binary values; every bits store to sublist
    bit_seq +=  f"{byte:08b}"
#conv encode
code = conv_code.encoder(bit_seq)
print()
print('code before transmission: {}'.format(code))
import random
code_ = bitarray(code)
for _ in range(5):
    idx = random.randint(0, len(code) - 1)
    code_[idx] = not (code_[idx])
code_ = str(code_)[10:-2]
print('code after  transmission: {}'.format(code_))
print('before transmission == after transmission: {}'.format(code == code_))
send_msg(code_)
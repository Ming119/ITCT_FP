
# 從 gpiozero 模組當中載入 LED 功能
from gpiozero import LED
from time import sleep, time
import  sys, math
from grove.adc import ADC
from hamming_code import hamming_decode, hamming_encode
import conv_code
from bitarray import bitarray
from reedsolo import RSCodec, ReedSolomonError
led = LED(13)
__all__ = ["GroveLightSensor"]


def bytearray_to_bitarray(byte_array):
    bit_array = ''.join(format(byte, '08b') for byte in byte_array)
    return bit_array

def bitarray_to_bytearray(bit_array):
    # 將二進制字符串按8位分割，轉換為整數列表
    byte_values = [int(bit_array[i:i + 8], 2) for i in range(0, len(bit_array), 8)]

    # 將整數列表轉換為位元組陣列
    byte_array = bytearray(byte_values)

    return byte_array

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
    sleep(0.003)
    signal = 1
    while signal == 1:
      pass
  signal = -1



def read_light_rs_conv(channel, threshold):
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
        #conv decode
        d_code, corrected_errors = conv_code.decoder(m)
        print('conv corrected errors {}'.format(corrected_errors / 8))
        d_code = bitarray_to_bytearray(d_code)
        #rs decode
        try:
            result = rsc.decode(d_code)[0].decode('utf-8')
            print(result)
        except:
            print('Roo many errors, RS decode fail')
        flag = False
        m = ''
      else:
        pass

def send_msg(msg):
  thread2 = threading.Thread(target=led_light,args = [msg,])
  thread2.start()
  thread2.join()

def rs_conv_encode(msg, rsc):
    #msg_b len(msg) B
    msg_b = msg.encode("utf-8")
    
    print('length of msg',end = ': ')
    print(len(msg_b))
    #rs encode
    #rs_encode  (1+0.1 * X) * len(msg) B if tolerate 2 * X bits error
    rs_encode = bytearray_to_bitarray(rsc.encode(msg_b))
    print('length of rs code',end = ': ')
    print(len(rs_encode) / 8)
    #conv encode
    #conv code 2 * (rs code + 0.25) B if encode by 212 conv codec
    code = conv_code.encoder(rs_encode)
    import random
    code_ = bitarray(code)
    #random choose 4B index to flip
    print('length of conv code',end = ': ')
    print(len(code) / 8)
    number_range = list(range(len(code) - 1))
    random_numbers = random.sample(number_range, int(len(code) / 10))
    for i in random_numbers:
        code_[i] = not (code_[i])
    code_ = str(code_)[10:-2]
    return code_
from grove.helper import SlotHelper
import threading
sh = SlotHelper(SlotHelper.ADC)
pin = sh.argv2pin()
#test conv code
thread1 = threading.Thread(target=read_light_rs_conv,args = [pin,400,]).start()
rsc = RSCodec(10) #can tolerate 5 error
code_ = rs_conv_encode('hello word', rsc)
send_msg(code_)

print('wait 2 sec')
start = time()
while time() - start < 2:
  pass
print()

code_ = rs_conv_encode('ITCT final project', rsc)
send_msg(code_)


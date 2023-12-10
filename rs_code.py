from reedsolo import RSCodec, ReedSolomonError
import conv_code
from bitarray import bitarray

def bytearray_to_bitarray(byte_array):
    bit_array = ''.join(format(byte, '08b') for byte in byte_array)
    return bit_array

def bitarray_to_bytearray(bit_array):
    # 將二進制字符串按8位分割，轉換為整數列表
    byte_values = [int(bit_array[i:i + 8], 2) for i in range(0, len(bit_array), 8)]

    # 將整數列表轉換為位元組陣列
    byte_array = bytearray(byte_values)

    return byte_array

if __name__ == "__main__":
    rsc = RSCodec(20)
    #encode string to utf8
    print('input : hello word')
    msg_b = 'hello word'.encode("utf-8")
    #rs encode
    rs_encode = bytearray_to_bitarray(rsc.encode(msg_b))
    #conv encode
    code = conv_code.encoder(rs_encode)
    #Simulate transmission errors 
    print('code before transmission: {}'.format(code))
    #decode conv code
    d_code, corrected_errors = conv_code.decoder(code)
    #decode utf-8
    d_code = bitarray_to_bytearray(d_code)

    print(rsc.decode(d_code)[0].decode('utf-8'))



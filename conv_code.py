#implement 212 conv code
from bitarray import bitarray
import sys

#input bit string
def encoder(data):
    data = bitarray(data)
    #add 2 zero to flush register
    data += [0] * 2
    reg = bitarray('00')
    code = ''
    for i in data: 
        code += str(reg[1] ^ i)
        code += str(reg[0] ^ reg[1] ^ i)
        reg = reg >> 1 
        reg[0] = i
    return code

def decoder(code):
    F_bits = ['{}{}'.format(code[i * 2],code[i * 2+ 1]) for i in range(int(len(code) / 2))]
    state_dict = {
        '00': {'path':['00','00'],'distance':hamming_distance(F_bits[0],'00')},
        '10': {'path':['00','10'],'distance':hamming_distance(F_bits[0],'11')},
        '01': {'path':[],'distance':sys.maxsize},
        '11': {'path':[],'distance':sys.maxsize}
    }
    state_transform_dict = {
        '00' : [{'state':'00','value':'00'},{'state':'10','value':'11'}],
        '10' : [{'state':'01','value':'01'},{'state':'11','value':'10'}],
        '01' : [{'state':'00','value':'11'},{'state':'10','value':'00'}],
        '11' : [{'state':'01','value':'10'},{'state':'11','value':'01'}]
    }
    step = 0
    for step in range(1,len(F_bits)):
        temp_dict = {
            '00': {'path':[],'distance':sys.maxsize},
            '10': {'path':[],'distance':sys.maxsize},
            '01': {'path':[],'distance':sys.maxsize},
            '11': {'path':[],'distance':sys.maxsize}
        }
        for key in state_dict.keys():
            if state_dict[key]['path'] != []:
                for next_state in state_transform_dict[key]:
                    if temp_dict[next_state['state']]['distance'] > state_dict[key]['distance'] + hamming_distance(F_bits[step],next_state['value']):
                        temp_dict[next_state['state']]['distance'] = state_dict[key]['distance'] + hamming_distance(F_bits[step],next_state['value'])
                        temp_dict[next_state['state']]['path'] = state_dict[key]['path'].copy()
                        temp_dict[next_state['state']]['path'].append(next_state['state'])
        state_dict = temp_dict
    shortest_path = None
    for i in state_dict.keys():
        if shortest_path == None or state_dict[i]['distance'] < shortest_path['distance']:
            shortest_path = state_dict[i]
    ans = ''
    for i in range(1,len(shortest_path['path']) - 2):
        ans += shortest_path['path'][i][0]
    return ans
def hamming_distance(s1, s2):
    return sum(s1[i] != s2[i] for i in range(len(s1)))

if __name__ == "__main__":
    #encode string to utf8
    print('input : hello')
    msg_b = 'hello'.encode("utf-8")
    bit_seq = ''
    for byte in msg_b:  # get bytes to binary values; every bits store to sublist
        bit_seq +=  f"{byte:08b}"
    #conv encode
    code = encoder(bit_seq)
    #Simulate transmission errors 
    print('code before transmission: {}'.format(code))
    code_ = '0' + code[1:5] +'0'+code[6:-1] + '0'
    print('code after  transmission: {}'.format(code_))
    print('before transmission == after transmission: {}'.format(code == code_))
    #decode conv code
    d_code = decoder(code_)
    #decode utf-8
    msg_l = []
    for i in range(len(d_code) // 8):   # convert from binary-sring value to integer
        val = "".join(d_code[i * 8:i * 8 + 8])
        msg_l.append(int(val, 2))

    print('output: ' + bytes(msg_l).decode("utf-8"))   # finally decode to a regular string
def hamming_encode(data):
	data = list(''.join(format(ord(i), 'b') for i in data))

	# Calculate the number of parity bits needed
	m = len(data)
	r = 1
	while 2**r < m + r + 1:
		r += 1

	# Initialize the encoded data with zeros
	encoded_data = [0] * (m + r)

	# Copy the data bits into the correct positions
	j = 0
	for i in range(1, m + r + 1):
		if i == 2**j:
			j += 1
		else:
			encoded_data[i - 1] = int(data.pop(0))

	# Calculate the parity bits
	for i in range(r):
		index = 2**i - 1
		parity = 0
		for j in range(1, m + r + 1):
			if (j >> i) & 1:
				parity ^= encoded_data[j - 1]
		encoded_data[index] = parity

	return ''.join(map(str, encoded_data))

def hamming_decode(encoded_data):
	encoded_data = list(map(int, encoded_data))
	r = 1
	while 2**r < len(encoded_data) + 1:
		r += 1

	# Initialize the syndrome vector
	syndrome = [0] * r

	# Calculate the syndrome bits
	for i in range(r):
		parity = 0
		for j in range(len(encoded_data)):
			if (j + 1) & (2**i):
				parity ^= encoded_data[j]
		syndrome[i] = parity

	# Correct the error, if any
	error_position = sum([2**i * syndrome[i] for i in range(r)])
	if error_position != 0:
		encoded_data[error_position - 1] ^= 1

	# Extract the original data
	decoded_data = [encoded_data[i] for i in range(len(encoded_data)) if i & (i + 1) != 0]

	# bitarray to string
	decoded_data = ''.join(chr(int(decoded_data[i:i+8], 2)) for i in range(0, len(decoded_data), 8))

	return decoded_data

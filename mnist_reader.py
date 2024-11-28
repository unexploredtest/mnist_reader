
import numpy as np


# (data_size, data_type)
data_types = {
    0x8: (1, np.uint8),
    0x9: (1, np.int8),
    0xB: (2, np.int16),
    0xC: (4, np.int32),
    0xD: (4, np.float32),
    0xE: (8, np.float64)
}

def read_idx(file_data):
    array = None

    current_byte = 0
    current_byte += 2 # The first two bytes are useless so we pass

    data_type_info_b = file_data[current_byte:current_byte+1]
    current_byte += 1
    data_type_info = int.from_bytes(data_type_info_b, "big", signed=False)

    (data_size, data_type) = data_types[data_type_info]

    dim_number_b = file_data[current_byte:current_byte+1]
    current_byte += 1
    dim_number = int.from_bytes(dim_number_b, "big", signed=False)

    array_size = 1
    dimensions = [0]*dim_number
    for i in range(dim_number):
        dim_size_b = file_data[current_byte:current_byte+4]
        current_byte += 4
        dim_size = int.from_bytes(dim_size_b, "big", signed=False)
        dimensions[i] = dim_size
        array_size *= dim_size

    # IDX format uses big endian so we make numpy data types big endian
    dt = np.dtype(data_type)
    dt = dt.newbyteorder('>')
    array = np.frombuffer(file_data[current_byte:], dtype=dt)
    return array.reshape(dimensions)

def read_idx_file(file_path):
    file_data = None
    with open(file_path, "rb") as idx_file:
        file_data = idx_file.read()
    return read_idx(file_data)
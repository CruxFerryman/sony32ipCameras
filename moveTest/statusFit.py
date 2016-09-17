import numpy as np

velocity_base = 10
velocity_base_degree = 0.2

status_filename = 'inquiry.cgi?inq=ptzf'
degrees_per_hex_val = 0.022059
max_pan_degrees = 180
min_pan_degrees = -180
min_tilt_degrees = -110
max_tilt_degrees = 110
default_save_dir = './'
file_number = 5
file_name_prefix = "status"
file_name_suffix = ".b"

ip_prefix = "10.1.201."
ip_table = [202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 239, 218, 219, 220, 221, 237,
            223, 224, 225, 226, 233, 228, 229, 230, 231, 232, 236]

fit_number = 5

for suffix in ip_table:
    index = ip_table.index(suffix)
    ip_table[index] = ip_prefix + str(suffix)

file_list = [object] * file_number


def read_status_file(file_prefix, file_num, file_suffix):
    pan_value = []
    tile_value = []
    file_name = file_prefix + str(file_num) + file_suffix
    file_path = default_save_dir + file_name
    with open(file_path, "rb") as file_stream:
        for line in file_stream:
            current_line = line.split(", ")
            pan_value.append(current_line[0])
            tile_value.append(current_line[1])
    return pan_value, tile_value


def save_status_to_list(file_n):
    pan_values = [] * file_n
    tilt_values = [] * file_n
    for num in range(file_n):
        p_tmp, t_tmp = read_status_file(file_name_prefix, num + 1, file_name_suffix)
        pan_values.append(p_tmp)
        tilt_values.append(t_tmp)
    return pan_values, tilt_values


p, t = save_status_to_list(file_number)

functions = []
for ip in ip_table:
    index = ip_table.index(ip)
    p_ip_values = []
    t_ip_values = []
    for status_num in range(file_number):
        p_ip_values.append(float(p[status_num][index]) / degrees_per_hex_val)
        t_ip_values.append(float(t[status_num][index]) / degrees_per_hex_val)
    #    print(p_ip_values, t_ip_values)
    x = np.array(p_ip_values)
    y = np.array(t_ip_values)
    f = np.polyfit(x, y, 2)
    functions.append(f)

for status_fit in range(file_number + 1, file_number + 1 + fit_number):
    index = status_fit - 1 - fit_number
    function = functions[status_fit]

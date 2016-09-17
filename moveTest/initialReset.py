from multiprocessing import Pool

import requests

velocity_base = 12
velocity_base_degree = 0.2

status_filename = 'inquiry.cgi?inq=ptzf'
degrees_per_hex_val = 0.022059
max_pan_degrees = 180
min_pan_degrees = -180
min_tilt_degrees = -110
max_tilt_degrees = 110
default_save_dir = './'
file_number = 9
file_name_prefix = "status"
file_name_suffix = ".b"

ip_prefix = "10.1.201."
ip_table = [202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 239, 218, 219, 220, 221, 237,
            223, 224, 225, 226, 233, 228, 229, 230, 231, 232, 236]

for suffix in ip_table:
    index = ip_table.index(suffix)
    ip_table[index] = ip_prefix + str(suffix)

file_list = [object] * file_number


def change2padhex(stringin):
    temp = hex(int(stringin))
    qq = len(temp)
    hexstring = ''
    for i in range(qq, 6):
        hexstring = hexstring + '0'
    for i in range(2, qq):
        hexstring = hexstring + temp[i]
    return hexstring


def convertPanToHex(inputdegrees):
    if (inputdegrees > max_pan_degrees):
        inputdegrees -= 360
    if (inputdegrees < min_pan_degrees):
        inputdegrees += 360
    signedIntVal = inputdegrees / degrees_per_hex_val
    if (signedIntVal < 0):
        signedIntVal += pow(2, 16)
    hexString = change2padhex(signedIntVal)
    return hexString


def convertPanToDegrees(inputhex):
    unsignedIntVal = int(inputhex, 16)
    if (unsignedIntVal >= pow(2, 15)):
        signedIntVal = unsignedIntVal - pow(2, 16)
    else:
        signedIntVal = unsignedIntVal
    panDegrees = float(signedIntVal) * degrees_per_hex_val
    if panDegrees > max_pan_degrees:
        print('Something is wrong, pan degree setting is out of range')
    if panDegrees < min_pan_degrees:
        print('Something is wrong, pan degree setting is out of range')
    return panDegrees


def convertUnsignedToSigned(inputhex):
    unsignedIntVal = int(inputhex, 16)
    if (unsignedIntVal >= pow(2, 15)):
        signedIntVal = unsignedIntVal - pow(2, 16)
    else:
        signedIntVal = unsignedIntVal
    return signedIntVal


def convertTiltToHex(inputdegrees):
    signedIntVal = inputdegrees / degrees_per_hex_val
    hexString = change2padhex(signedIntVal)
    return (hexString)


def convertTiltToDegrees(inputhex):
    unsignedIntVal = int(inputhex, 16)
    if (unsignedIntVal >= pow(2, 15)):
        signedIntVal = unsignedIntVal - pow(2, 16)
    else:
        signedIntVal = unsignedIntVal
    tiltDegrees = float(signedIntVal) * degrees_per_hex_val
    if tiltDegrees > max_pan_degrees:
        print('Something is wrong, pan degree setting is out of range')
    if tiltDegrees < min_tilt_degrees:
        print('Something is wrong, pan degree setting is out of range')
    return tiltDegrees


def hexchangePT(ip, newpan, newtilt):
    status_ip = 'http://' + str(ip) + '/command/' + status_filename
    r_status = requests.get(status_ip, auth=('admin', 'admin'))
    nowpan = convertPanToDegrees(r_status.text[13:17])
    nowtilt = convertTiltToDegrees(r_status.text[18:22])
    pan_sub = abs(float(newpan) - float(nowpan))
    tilt_sub = (float(newtilt) - float(nowtilt))
    #    velocity = int((abs(pan_sub/velocity_base_degree) + abs(tilt_sub/velocity_base_degree))*velocity_base/2/10)
    #     velocity = int(pan_sub*2)
    #     if velocity >= 10:
    #         velocity = 9
    #     elif velocity <= 8:
    #         velocity = 8
    if pan_sub > 1:
        velocity = 9
    else:
        velocity = 7
    newpan_hex = convertPanToHex(float(newpan))
    newtilt_hex = convertTiltToHex(float(newtilt))
    url = 'http://' + ip + '/command/ptzf.cgi?AbsolutePanTilt='
    r = requests.get(url + str(newpan_hex) + ',' + str(newtilt_hex) + ',' + str(velocity), auth=('admin', 'admin'))
    print ip, velocity, r


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


def continous_roll(ip_address, pan_values_list, tilt_values_list):
    url_zoom = 'http://' + ip_address + '/command/ptzf.cgi?&AbsoluteZoom='
    requests.get(url_zoom + b'13c4', auth=('admin', 'admin'))
    url = 'http://' + ip_address + '/command/ptzf.cgi?AbsolutePanTilt='
    for status_number in range(file_number):
        new_pan_hex = convertPanToHex(float(pan_values_list[status_number]))
        new_tilt_hex = convertTiltToHex(float(tilt_values_list[status_number]))
        r = requests.get(url + str(new_pan_hex) + ',' + str(new_tilt_hex) + ',' + str(velocity_base),
                         auth=('admin', 'admin'))
    #        print(ip_address, status_number, r)
    return


if __name__ == '__main__':
    p, t = save_status_to_list(file_number)
    pool_ip_continous = Pool(len(ip_table))
    for ip in ip_table:
        index = ip_table.index(ip)
        p_ip_values = []
        t_ip_values = []
        for status_num in range(file_number):
            p_ip_values.append(p[0][index])
            t_ip_values.append(t[0][index])
        pool_ip_continous.apply_async(continous_roll, args=(ip, p_ip_values, t_ip_values))
    pool_ip_continous.close()
    pool_ip_continous.join()

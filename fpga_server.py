import socket
import numpy as np
import time
import os
import time
from threading import Thread
from global_var import put_into_queue, get_from_queue, get_queue_remainder


def start_fpga_server(server_ip = "192.168.1.102", server_port = 8080,
                    client_ip = "192.168.1.100", client_port = 8080,
                    post_freq = 1):

    """
    To start FPGA server to collect UDP package, and put the data into a global queue. 
    """

    # initialize parameters
    BUFSIZE = 2048
    server_ip_port = (server_ip, server_port)
    client_ip_port = (client_ip, client_port)
    
    # initialize server
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(server_ip_port)

    # generate msg_start_sending to shake hand
    msg_start_sending = "\x28\x00\x01\x00\x02\x01\xA0\x35\x00\x01\x02\x00\x00\x00\x01\x00\x00\x80\x00"

    # send start message
    print(server.sendto(msg_start_sending.encode("latin-1"), client_ip_port)) # latin-1 can avoid \xc2

    count = 0
    data_buffer = None
    while True:
        data, client_addr = server.recvfrom(BUFSIZE)
        count += 1
        # print(count)

        if data_buffer is None:
            data_buffer = data
        else:
            data_buffer += data

        if count % int(64 / post_freq / 2) == 0:
            processed_data = processing_data(data_buffer)
            print(processed_data.shape)
            put_into_queue(processed_data)
            data_buffer = None
            print("1 frame")


def processing_data(raw_data):

    """Convert raw data to 8 dimensions
    input: raw data
    return: numpy array
    """
    
    data = np.frombuffer(raw_data, np.uint8)
    data = np.reshape(data, [data.shape[0]//1029, -1])
    data = data[:, 5:]
    data = np.reshape(data, [1, -1])
    data = 256 * data[0, 0::2] + data[0, 1::2]
    data = 10 * (data / 65535)
    data = np.reshape(data, [-1, 8]).T
    return data


def temp_output():
    while True:
        time.sleep(1/32)
        print(get_from_queue().shape)
        print(get_queue_remainder(), time.time())


if __name__ == "__main__":

    args = {
        "server_ip" : "192.168.1.102",
        "post_freq" : 1,
    }
    server = Thread(target=start_fpga_server, kwargs=args)
    output = Thread(target=temp_output)
    server.start()
    output.start()

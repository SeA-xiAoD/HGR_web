from django.shortcuts import render
from django.http import JsonResponse, FileResponse
import json
from global_var import get_from_queue, get_queue_remainder, store_off_switch, store_on_switch, get_switch
import os
import time
import numpy as np
from fpga_server import start_fpga_server, temp_output
from multiprocessing import Process
from threading import Thread

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


def display(request):
    global args
    args = {
        "server_ip" : "192.168.1.102",
        "post_freq" : 0.5,
    }
    fpga_server_thread = Thread(target=start_fpga_server, kwargs=args)
    fpga_server_thread.start()
    return render(request, 'display.html')


def query_data(requset):
    dic = {}
    data = get_from_queue()
    data = data[:,::32]
    print(data.shape, get_queue_remainder())
    dic["data"] = data.tolist()
    json_dump = json.dumps(dic)
    return JsonResponse(json_dump, safe=False)


def store_on(request):
    store_on_switch()
    dic = {}
    dic["success"] = True
    json_dump = json.dumps(dic)
    return JsonResponse(json_dump, safe=False)


def store_off(request):
    store_off_switch()
    dic = {}
    dic["success"] = True
    json_dump = json.dumps(dic)
    return JsonResponse(json_dump, safe=False)
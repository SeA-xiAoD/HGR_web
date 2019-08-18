from django.shortcuts import render
from django.http import JsonResponse, FileResponse
import json
import  global_var as global_dict
import os
import time
import numpy as np
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


def display(request):
    return render(request, 'display.html')


def query_data(requset):
    dic = {}
    data = np.random.rand(8, 100)
    dic["data"] = data.tolist()
    json_dump = json.dumps(dic)
    return JsonResponse(json_dump, safe=False)
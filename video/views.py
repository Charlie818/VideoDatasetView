# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from util import *
import json
import os
import sys
# Create your views here.

JSON_FILE = os.path.join(os.path.join(
    sys.path[0], "video", "static", "dataset", "video.json"))
with open(JSON_FILE, 'r') as fr:
    json_data = json.load(fr)

def index(request):
    context = {'data': json.dumps(json_data)}
    return render(request, 'index.html', context=context)

def video_request(request):
    ret=get_video(request.POST['file'],json_data)
    return HttpResponse(json.dumps(ret))

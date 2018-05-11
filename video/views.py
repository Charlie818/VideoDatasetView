# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from util import get_video
import json
import os
import sys
# Create your views here.

JSON_FILE = os.path.join(os.path.join(
    sys.path[0], "video", "static", "dataset", "val.json"))
with open(JSON_FILE, 'r') as fr:
    groundtruth = json.load(fr)
JSON_FILE2 = os.path.join(os.path.join(
    sys.path[0], "video", "static", "dataset", "result.json"))
with open(JSON_FILE2, 'r') as fr:
    proposals = json.load(fr)

def index(request):
    names=[name for name in groundtruth]
    selected=names[0]
    sample=groundtruth[selected]
    sample['predicts']=proposals.get(selected,{}).get("proposal",[])
    print
    data={'name':names,'sample':sample}
    context = {'data':json.dumps(data)}
    # context = {'groundtruth': json.dumps(groundtruth),'proposals':json.dumps(proposals)}
    return render(request, 'index.html', context=context)

def video_request(request):
    ret=get_video(request.POST['file'],groundtruth,proposals)
    return HttpResponse(json.dumps(ret))

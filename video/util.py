from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import os

DIR=os.path.join(os.getcwd(),"static","dataset")
JSON_FILE = os.path.join(DIR, "val.json")

class Proprosal(object):
    """docstring for Proprosal"""

    def __init__(self, start_time, end_time, annotation):
        super(Proprosal, self).__init__()
        self.start_time = start_time
        self.end_time = end_time
        self.annotation = annotation

    def convert(self):
        return {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "annotation": self.annotation
        }

class Video(object):
    """docstring for Video"""

    def __init__(self, path, name, proposals,duration):
        super(Video, self).__init__()
        self.path = path
        self.name = name
        self.proposals = proposals
        file=self.path.split('/')[-1]
        self.url = os.path.join("dataset","links",file)
        self.duration=duration

    def convert(self):
        return {
            "path": self.path,
            "name": self.name,
            "proposals": self.proposals,
            "url": self.url,
            "duration":self.duration
        }

def get_file_list(path, _except=[], sort=True):
    _except.append('.DS_Store')
    if sort:
        return sorted(
            [os.path.join(path, x) for x in os.listdir(path) if os.path.isfile(os.path.join(path, x)) and x not in _except])
    else:
        return [os.path.join(path, x) for x in os.listdir(path) if
                os.path.isfile(os.path.join(path, x)) and x != _except]

def create_json(infile,outfile):
    with open(infile, 'r') as fr:
        data=json.load(fr)
    res={}
    for video in data:
        info=data[video]
        assert len(info['timestamps'])==len(info['sentences'])
        proposals_cnt=len(info['timestamps'])
        proposals=[]
        for i in range(proposals_cnt):
            start_time,end_time=info['timestamps'][i]
            sentences=info['sentences'][i]
            #TODO:annotation should be its categeory
            annotation=info['sentences'][i]
            proposals.append(Proprosal(start_time,end_time,annotation).convert())
        # if os.path.isfile(os.path.join(DIR, video+'.mp4')):
        res[video]=Video(os.path.join(DIR, 'links', video+'.mp4'),video,proposals,info['duration']).convert()
        # res.append(Video(os.path.join(DIR, video+'.mp4'),video,proposals,info['duration']).convert())

    with open(outfile, 'w') as fw:
        json.dump(res, fw)


def get_video(filename,groundtruth,proposals):
    ret=groundtruth[filename]
    predicts=proposals.get(filename,{}).get('proposal',[])
    ret['predicts']=predicts
    return ret

def create_symbolic_link(src_dir):
    files=[ x for x in os.listdir(src_dir) if os.path.isfile(os.path.join(src_dir, x)) and x.endswith('.mp4')]
    for file in files:
        infile=os.path.join(src_dir,file)
        outfile=os.path.join(DIR,file)
        str = "ln -s %s %s"%(infile,outfile)
        os.system(str)

def create_sample_video(src_dir,dest_dir):
    def video_simplify(infile,outfile):
        str = "ffmpeg -i %s -an -s 160*120 -r 5 %s"%(infile,outfile)
        os.system("rm %s"%(outfile))
        os.system(str)
    for infile in get_file_list(src_dir):
        filename =infile.split('/')[-1]
        outfile = os.path.join(dest_dir,filename)
        video_simplify(infile,outfile)

def preprocess():
    # create_json(infile='/data1/densevid/captions/val_1.json',outfile=JSON_FILE)
    # create_sample_video(src_dir="/data1/densevid/videos/val",dest_dir="/root/samples/val")
    create_symbolic_link(src_dir="/data1/qiujiarong/samples/val")
    pass
def main():
    preprocess()

if __name__ == '__main__':
    main()

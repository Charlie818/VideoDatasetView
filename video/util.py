from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import os

DIR=os.path.join(os.getcwd(),"static","dataset")
JSON_FILE = os.path.join(DIR, "video.json")

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
        folder=self.path.split('/')[-2]
        self.url = os.path.join(folder+'/'+file)
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

def create_json():
    p11 = Proprosal(1, 4, "P11 annotation").convert()
    p12 = Proprosal(3, 6, "P12 annotation").convert()
    p21 = Proprosal(3, 4, "P21 annotation").convert()
    v1 = Video(os.path.join(DIR, "test1.mp4"), "test1", [p11,p12],10).convert()
    v2 = Video(os.path.join(DIR, "test2.mp4"), "test2", [p21],10).convert()
    data = [v1, v2]
    with open(JSON_FILE, 'w') as fw:
        json.dump(data, fw)


def load_json():
    with open(JSON_FILE, 'r') as fr:
        return json.load(fr)

def get_video(filename,json_data):
    ret=[i for i in json_data if i['name']==filename][0]
    return ret


def main():
    create_json()
    # json_data=load_json()
    # print(get_video("test2",json_data))


if __name__ == '__main__':
    main()

# VideoDatasetView

Implement ActivityNet Captions validation dataset

input: {val/result}.json
shall locate at video/static/dataset/

format:
{
    "video_id":{
        "name":
        "path":
        "duration":
        "proposals":[
            {
            "start_time":
            "end_time":
            "annotation":
            }
        ]

    }
}
Note that name,path and duration are not necessary for result.json 

Functionality:
view videos
show groundtruth and proposals in red and green lines
show annotation and captions in the left


Set up the system:
    uwsgi --ini /root/VideoView/uwsgi.ini
    nginx -c /root/VideoView/nginx.conf


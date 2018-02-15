import json
from shlex import quote
import wrap
import subprocess
import requests


def down_and_send(v_id, ID):
    try:
        subprocess.run("youtube-dl --write-info-json --geo-bypass -o \"Download/%(id)s/video.%(ext)s\" "
                       "-f mp4 {}".format(quote(v_id)), shell=1)
        js = json.load(open("Download/"+v_id+"/video.info.json"))
        resp = wrap.get_video_link(js['title'], js['description'])
        f = open("Download/"+v_id+"/video.mp4", 'rb')
        r = requests.post(url=resp['upload_url']
                          , files={'file': f})
        wrap.send_attachment(ID, "", "video470444116_"+str(r.json()['video_id']))
        subprocess.run("rm -rf Download/{}".format(quote(v_id)), shell=1)
        return "--done--"
    except:
        subprocess.run("rm -rf Download/{}".format(quote(v_id)), shell=1)
        return "--error--"

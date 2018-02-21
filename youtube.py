# -*- coding: utf-8 -*-

import json
from shlex import quote
from wrap import VkWrap
import subprocess
import requests


def down_and_send(v_id, ID, bot):
    try:
        bot.send_message(ID, "--Запрос принят, ожидайте--")
        out = subprocess.run("youtube-dl --write-info-json --geo-bypass --max-filesize 300m "
                       "-o \"Download/%(id)s/video.%(ext)s\" "
                       "-f mp4 {}".format(quote(v_id)), shell=1, stdout=subprocess.PIPE).stdout
        print(out)
        js = json.load(open("Download/"+v_id+"/video.info.json"))
        resp = bot.get_video_link(js['title'], js['description'])
        f = open("Download/"+v_id+"/video.mp4", 'rb')
        r = requests.post(url=resp['upload_url']
                          , files={'file': f})
        bot.send_attachment(ID, "", "video470444116_"+str(r.json()['video_id']))
        subprocess.run("rm -rf Download/{}".format(quote(v_id)), shell=1)
        return "--done--"
    except:
        if out.find(b'File is larger than max-filesize'):
            try:
                subprocess.run("rm -rf Download/{}".format(quote(v_id)), shell=1)
                bot.send_message(ID, "--Лучшее качество занимает слишком много места, переход на худшее--")
                subprocess.run("youtube-dl --write-info-json --geo-bypass --max-filesize 300m "
                               "-o \"Download/%(id)s/video.%(ext)s\" "
                               "-f \"worst/mp4\" {}".format(quote(v_id)), shell=1)
                js = json.load(open("Download/" + v_id + "/video.info.json"))
                resp = bot.get_video_link(js['title'], js['description'])
                f = open("Download/" + v_id + "/video.mp4", 'rb')
                r = requests.post(url=resp['upload_url']
                                  , files={'file': f})
                bot.send_attachment(ID, "", "video470444116_" + str(r.json()['video_id']))
                subprocess.run("rm -rf Download/{}".format(quote(v_id)), shell=1)
                return "--done--"
            except:
                subprocess.run("rm -rf Download/{}".format(quote(v_id)), shell=1)
                return "--error--"
        subprocess.run("rm -rf Download/{}".format(quote(v_id)), shell=1)
        return "--error--"

# -*- coding: utf-8 -*-

import json
from shlex import quote
from wrap import VkWrap
import subprocess
import requests


def down_and_send(v_id, chat_id, bot):
    try:
        bot.send_message(chat_id, "--Запрос принят, ожидайте--")
        out = subprocess.run(
            args=['youtube-dl', '--write-info-json', '--geo-bypass', '--max-filesize 300m',
                  '-o \"Download/%(id)s/video.%(ext)s\"', '-f mp4 {}'.format(quote(v_id))],
            shell=True,
            stdout=subprocess.PIPE
        ).stdout
        print(out)
        js = json.load(open("Download/" + v_id + "/video.info.json"))
        resp = bot.get_video_link(js['title'], js['description'])
        f = open("Download/" + v_id + "/video.mp4", 'rb')
        r = requests.post(url=resp['upload_url']
                          , files={'file': f})
        bot.send_attachment(chat_id, "", "video" + str(bot.me) + "_" + str(r.json()['video_id']))
        subprocess.run("rm -rf Download/{}".format(quote(v_id)), shell=True)
        return "--done--"
    except:
        if out.find(b'File is larger than max file size'):
            try:
                subprocess.run("rm -rf Download/{}".format(quote(v_id)), shell=True)
                bot.send_message(chat_id, "--Лучшее качество занимает слишком много места, переход на худшее--")
                subprocess.run("youtube-dl --write-info-json --geo-bypass --max-filesize 300m "
                               "-o \"Download/%(id)s/video.%(ext)s\" "
                               "-f \"worst/mp4\" {}".format(quote(v_id)), shell=True)
                js = json.load(open("Download/" + v_id + "/video.info.json"))
                resp = bot.get_video_link(js['title'], js['description'])
                f = open("Download/" + v_id + "/video.mp4", 'rb')
                r = requests.post(url=resp['upload_url']
                                  , files={'file': f})
                bot.send_attachment(chat_id, "", "video470444116_" + str(r.json()['video_id']))
                subprocess.run("rm -rf Download/{}".format(quote(v_id)), shell=True)
                return "--done--"
            except:
                subprocess.run("rm -rf Download/{}".format(quote(v_id)), shell=True)
                return "--error--"
        subprocess.run("rm -rf Download/{}".format(quote(v_id)), shell=True)
        return "--error--"

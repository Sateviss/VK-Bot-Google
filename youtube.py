# -*- coding: utf-8 -*-

import json
from shlex import quote
from wrap import VkWrap
import subprocess
import requests


def down_and_send(v_id, chat_id, bot: VkWrap):
    global out
    try:
        bot.send_message(chat_id, "Запрос принят, ожидайте")
        out = subprocess.run(
            args=["youtube-dl --write-info-json --geo-bypass --max-filesize 300m "
                  " -o \"Download/%(id)s/video.%(ext)s\" -f mp4 {0}".format(quote(v_id))],
            shell=True,
            stdout=subprocess.PIPE
        ).stdout
        print(out)
        js = json.load(open("Download/{0}/video.info.json".format(v_id)))
        resp = bot.get_video_link(js['title'], js['description'])
        f = open("Download/{0}/video.mp4".format(v_id), 'rb')
        r = requests.post(url=resp['upload_url'], files={'file': f})
        bot.send_attachment(chat_id, "", "video" + str(bot.me) + "_" + str(r.json()['video_id']))
        subprocess.run("rm -rf Download/{}".format(quote(v_id)), shell=True)
        return "done"
    except Exception as e:
        if b'File is larger than max-filesize' in out:
            try:
                subprocess.run("rm -rf Download/{}".format(quote(v_id)), shell=True)
                bot.send_message(chat_id, "Лучшее качество занимает слишком много места, переход на худшее")
                subprocess.run("youtube-dl --write-info-json --geo-bypass --max-filesize 300m "
                               "-o \"Download/%(id)s/video.%(ext)s\" "
                               "-f \"worst[ext=mp4]\" {}".format(quote(v_id)), shell=True)
                js = json.load(open("Download/" + v_id + "/video.info.json"))
                resp = bot.get_video_link(js['title'], js['description'])
                f = open("Download/" + v_id + "/video.mp4", 'rb')
                r = requests.post(url=resp['upload_url'], files={'file': f})
                bot.send_attachment(chat_id, "", "video{0}_{1}".format(r.json()['owner_id'], r.json()['video_id']))
                subprocess.run("rm -rf Download/{}".format(quote(v_id)), shell=True)
                return "done"
            except Exception as e:
                subprocess.run("rm -rf Download/{}".format(quote(v_id)), shell=True)
                raise e
        subprocess.run("rm -rf Download/{}".format(quote(v_id)), shell=True)
        raise e

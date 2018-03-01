#!/usr/bin/python3
# -*- coding: utf-8 -*-

import vk
import time
import sys


def delay_dec(func):
    def func_wrapper(*args, **kwargs):
        delay = 0.01
        while 1:
            try:
                return func(*args, **kwargs)
            except:
                if delay > 10:
                    return "err"
                time.sleep(delay)
                delay *= 2
    return func_wrapper


class VkWrap:

    def __init__(self, login, password):
        self.api = self.log_in(login, password)
        self.user_dict = {}
        self.me = self.get_user()['uid']

    def log_in(self, login, password):
        session = vk.AuthSession(app_id=6386090, user_login=login, user_password=password, scope=268435455)
        return vk.API(session)

    @delay_dec
    def doc_get_url(self):
        return self.api.docs.getUploadServer()['upload_url']

    @delay_dec
    def doc_save(self, link):
        return self.api.docs.save(file=link)

    @delay_dec
    def execute(self, c):
        return self.api.execute(code = c)

    @delay_dec
    def get_history(self, c_id):
        return self.api.messages.getHistory(chat_id=c_id, count=1)[1]

    @delay_dec
    def get_inbox(self, lm = None):
        if lm == None:
            return self.api.messages.get(count=1)[1]
        else:
            mess = self.api.messages.get(count=200, last_message_id=lm)
            mess.pop(0)
            return mess

    @delay_dec
    def send_message(self, c_id, text):
        if int(c_id) > 100000:
            if self.get_user(c_id)['can_write_private_message'] == 0:
                return "err"

        if len(text) < 4000:
            if int(c_id) > 100000:
                m = self.api.messages.send(user_id=c_id, message=text)
            else:
                m = self.api.messages.send(chat_id=c_id, message=text)
        else:
            if int(c_id) > 100000:
                m = self.api.messages.send(user_id=c_id, message="Очень длинное сообщение, которое начинается на "+text[:200])
            else:
                m = self.api.messages.send(chat_id=c_id, message="Очень длинное сообщение, которое начинается на "+text[:200])
        return m

    @delay_dec
    def send_attachment(self, c_id, text, att):
        if int(c_id) > 100000:
            if self.get_user(c_id)['can_write_private_message'] == 0:
                return "err"
        if len(text) < 4000:
            if int(c_id) > 100000:
                m = self.api.messages.send(user_id=c_id, message=text, attachment=att)
            else:
                m = self.api.messages.send(chat_id=c_id, message=text, attachment=att)
        else:
            if int(c_id) > 100000:
                m = self.api.messages.send(user_id=c_id, message="Очень длинное сообщение, которое начинается на "+text[:200]
                                           , attachment=att)
            else:
                m = self.api.messages.send(chat_id=c_id, message="Очень длинное сообщение, которое начинается на "+text[:200]
                                           , attachment=att)
        return m

    @delay_dec
    def delete_message(self, m_id):
        return self.api.messages.delete(message_ids=m_id, delete_for_all=1)

    @delay_dec
    def get_user(self, u_id=None):
        if self.user_dict.keys().__contains__(u_id):
            return self.user_dict[u_id]
        if u_id is not None:
            u = self.api.users.get(user_id=u_id, fields="photo_id, verified, sex, bdate, city, country, home_town, "
                                                   "has_photo, photo_50, photo_100, photo_200_orig, photo_200, "
                                                   "photo_400_orig, photo_max, photo_max_orig, online, domain, "
                                                   "has_mobile, contacts, site, education, universities, "
                                                   "schools, status, last_seen, followers_count, common_count, "
                                                   "occupation, nickname, relatives, relation, personal, "
                                                   "connections, exports, wall_comments, activities, interests,"
                                                   " music, movies, tv, books, games, about, quotes, can_post, "
                                                   "can_see_all_posts, can_see_audio, can_write_private_message"
                                                   ", can_send_friend_request, is_favorite, is_hidden_from_feed"
                                                   ", timezone, screen_name, maiden_name, crop_photo, is_friend"
                                                   ", friend_status, career, military, blacklisted, "
                                                   "blacklisted_by_me")[0]
        else:
            u = self.api.users.get()[0]
            self.user_dict.update({u_id: u})
        return u

    @delay_dec
    def msg_search(self, text, c, o):
        a = self.api.messages.search(q=text, count=c, offset=o)
        a.pop(0)
        return a

    def gen_sage(self, n):
        o = ''
        for i in range(n - 2):
            i += 2
            o += str(i) + ": "
            k = []
            x = 2
            while i != 1:
                if i % x == 0:
                    i /= x
                    k.append(x)
                    x = 1
                x += 1
            o += str(k) + "\n"
        return o

    @delay_dec
    def get_video_link(self, name_, description_):
        return self.api.video.save(name=name_, description=description_, wallpost=0, no_comments=1, privacy_view="friends_of_friends")

    @delay_dec
    def get_photo_link(self):
        return self.api.photos.getMessagesUploadServer()

    @delay_dec
    def save_photo(self, **kwargs):
        return self.api.photos.saveMessagesPhoto(**kwargs)[0]

    @delay_dec
    def get_friend(self, u_id):
        return self.api.friends.get(user_id=u_id)

    @delay_dec
    def delete_video(self, v_id):
        return self.api.video.delete(video_id=v_id)

    @delay_dec
    def cleanup_videos(self, s):
        vids = self.api.video.get()
        vids.pop(0)
        i = 0
        while i < len(vids):
            if vids[i]['date'] < time.time()-s:
                self.delete_video(vids[i]['vid'])
            else:
                i += 1
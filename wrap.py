# -*- coding: utf-8 -*-

import vk
import time

api = vk.API
user_dict = {}


def log_in(login, password):
    session = vk.AuthSession(app_id=6322567, user_login=login, user_password=password, scope=268435455)
    global api
    api = vk.API(session)


def get_history(c_id):
    delay = 0.01
    while 1:
        try:
            mess = api.messages.getHistory(chat_id=c_id, count=1)[1]
            return mess
        except:
            time.sleep(delay)
            delay *= 2
            continue


def get_inbox():
    delay = 0.01
    while 1:
        try:
            mess = api.messages.get(count=1)[1]
            return mess
        except:
            time.sleep(delay)
            delay *= 2
            continue


def send_message(c_id, text):
    delay = 0.01
    if int(c_id) > 100000000:
        if get_user(c_id)['can_write_private_message'] == 0:
            return "err"
    while 1:
        try:
            if len(text) < 4000:
                if int(c_id) > 100000000:
                    m = api.messages.send(user_id=c_id, message=text)
                else:
                    m = api.messages.send(chat_id=c_id, message=text)
            else:
                if int(c_id) > 100000000:
                    m = api.messages.send(user_id=c_id, message="Очень длинное сообщение, которое начинается на "+text[:200])
                else:
                    m = api.messages.send(chat_id=c_id, message="Очень длинное сообщение, которое начинается на "+text[:200])
            return m
        except:
            time.sleep(delay)
            delay *= 2
            continue


def send_attachment(c_id, text, att):
    delay = 0.01
    if int(c_id) > 100000000:
        if get_user(c_id)['can_write_private_message'] == 0:
            return "err"
    while 1:
        try:
            if len(text) < 4000:
                if int(c_id) > 100000000:
                    m = api.messages.send(user_id=c_id, message=text, attachment=att)
                else:
                    m = api.messages.send(chat_id=c_id, message=text, attachment=att)
            else:
                if int(c_id) > 100000000:
                    m = api.messages.send(user_id=c_id, message="Очень длинное сообщение, которое начинается на "+text[:200])
                else:
                    m = api.messages.send(chat_id=c_id, message="Очень длинное сообщение, которое начинается на "+text[:200])
            return m
        except:
            time.sleep(delay)
            delay *= 2
            continue


def delete_message(m_id):
    delay = 0.01
    while 1:
        try:
            api.messages.delete(message_ids=m_id, delete_for_all=1)
            return
        except:
            time.sleep(delay)
            delay *= 2
            continue


def get_user(u_id=None):
    delay = 0.01
    if user_dict.keys().__contains__(u_id):
        return user_dict[u_id]
    else:
        while 1:
            try:
                if u_id is not None:
                    u = api.users.get(user_id=u_id, fields="photo_id, verified, sex, bdate, city, country, home_town, "
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
                    u = api.users.get()[0]
                user_dict.update({u_id: u})
                return u
            except:
                time.sleep(delay)
                delay *= 2
                continue


def gen_message(n):
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


def get_video_link(name_, description_):
    delay = 0.01
    while 1:
        try:
            link = api.video.save(name=name_, description=description_, wallpost=0, no_comments=1,privacy_view="friends_of_friends_only")
            return link
        except:
            time.sleep(delay)
            delay *= 2
            continue


def delete_video(v_id):
    delay = 0.01
    while 1:
        try:
            api.video.delete(video_id=v_id)
            return
        except:
            time.sleep(delay)
            delay *= 2
            continue

def cleanup_videos(s):
    delay = 0.01
    while 1:
        try:
            vids = api.video.get()
            break
        except:
            time.sleep(delay)
            delay *= 2
            continue
    vids.pop(0)
    i = 0
    while i < len(vids):
        if vids[i]['date'] < time.time()-s:
            delete_video(vids[i]['vid'])
        else:
            i += 1
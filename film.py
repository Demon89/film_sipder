# _*_coding: utf-8_*_
"""
-------------------------------------------------
   File Name：     film
   Description :
   Author :        demon
   date：          03/03/2018
-------------------------------------------------
   Change Activity:
                   03/03/2018:
-------------------------------------------------
"""
__author__ = 'demon'

import os
import sys

import requests
from tqdm import tqdm

from bt_spider import sql_helper, sync_film_db


def search(film_name):
    result = sql_helper(film_name, sql_type='select')
    if result:
        for name, bt_url, bt_name in result:
            print('电影名称：', name)
            print('种子名称：', bt_name)
            print('下载链接：', bt_url)
            print()
    else:
        print('没有找到您要找的电影哦~')


def torrent_download(film_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    torrent_download_dir = current_dir + '/torrent'
    '' if os.path.exists(torrent_download_dir) else os.mkdir(torrent_download_dir)
    result = sql_helper(film_name.strip(), sql_type='select')
    if result:
        for name, torrent_url, torrent_name in tqdm(result):
            with requests.get(torrent_url) as req:
                torrent = req.content
            with open(torrent_download_dir + '/' + torrent_name, 'wb') as f:
                f.write(torrent)
    else:
        print('你要找的电影没有找到哦~~')


if __name__ == '__main__':
    parameter = len(sys.argv)
    if 1 <= parameter <= 3:
        command = sys.argv[1]
        try:
            film = sys.argv[2]
        except IndexError as e:
            film = ''
        if command == 'sync_db':
            sync_film_db()
        elif command == 'search' and film:
            search(film)
        elif command == 'download' and film:
            torrent_download(film)
        else:
            print('选项或者参数错误，请使用search 电影名称或者download 电影名称，如需同步，只需要执行sync_db')
    else:
        print('参数传递个数不对')



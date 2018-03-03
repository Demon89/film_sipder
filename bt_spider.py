# _*_coding: utf-8_*_
"""
-------------------------------------------------
   File Name：     bt_spider
   Description :
   Author :        demon
   date：          02/03/2018
-------------------------------------------------
   Change Activity:
                   02/03/2018:
-------------------------------------------------
"""
__author__ = 'demon'

import re
import csv
import asyncio
import cProfile

import pymysql
import aiohttp
from scrapy import Selector

MysqlDB = 'bt'
MysqlHost = '****'
MysqlUser = 'root'
MysqlPassword = '****'


def sql_helper(film, sql_type='select'):
    conn = pymysql.connect(host=MysqlHost, database=MysqlDB, user=MysqlUser, password=MysqlPassword, charset="utf8")
    cursor = conn.cursor()
    if sql_type == 'select':
        sql = 'select film, bt_url, bt_name from films where film like "%{film_name}%" or bt_name like "%{bt_name}%";'
        cursor.execute(sql.format(film_name=film, bt_name=film))
        result = set(cursor.fetchall())
        return result
    elif sql_type == 'insert':
        sql = 'insert into films (film,bt_name,bt_url) values("{}", "{}", "{}");'.format(*film)
        cursor.execute(sql.format(film_name=film, bt_name=film))
        cursor.close()
        conn.commit()

    else:
        raise TypeError('sql type must be select or insert')


async def html_source(url):
    async with aiohttp.request('GET', url) as req:
        source = await req.read()
    return source.decode()


def sync_film_db():
    conn = pymysql.connect(host=MysqlHost, database=MysqlDB, user=MysqlUser, password=MysqlPassword, charset="utf8")
    cursor = conn.cursor()
    sql = 'select * from films;'
    cursor.execute(sql)
    film_data = cursor.fetchall()
    with open('local_film.csv', 'a+', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerows(film_data)


class SaveFilm:

    def __init__(self):
        self.domain = 'http://www.btbtt.co/'

    async def get_film(self, url):
        source = await html_source(url)
        bt_url = re.findall(r'href="(attach-dialog-fid-.*\.htm)"', source)
        selector = Selector(text=source)
        film_name = selector.re(r'\[BT下载\].*B\b')
        film_name = film_name[0] if film_name else ''
        bt_name = selector.css('td:nth-child(1) > a::text').extract_first()
        if film_name and bt_name:
            return film_name, bt_name, self.domain + bt_url[0].replace('dialog', 'download')

    async def film_to_csv(self, film):
        with open('film.csv', 'a+', newline='', encoding='utf8') as f:
            writer = csv.writer(f)
            writer.writerow(film)

    async def film_to_mysql(self, film):
        sql_helper(film, 'insert')

    async def operations_films(self, url, page_num, save_type='mysql'):
        film_save = dict(csv=self.film_to_csv, mysql=self.film_to_mysql)
        source = await html_source(url.format(page_num))
        href = re.findall(r'href="(thread-index-fid-1183-tid.*\.htm)" target="_blank" ', source)
        film_href = (self.domain + url for url in href)
        for url in film_href:
            film = await self.get_film(url)
            if film:
                await film_save.get(save_type, 'csv')(film)

    def __repr__(self):
        return 'save bt films'

    def __call__(self, url, page_num, save_type='mysql'):
        return self.operations_films(url, page_num, save_type)


def main():
    base_url = 'http://btbtt.co/forum-index-fid-1183-page-{}.htm'
    loop = asyncio.get_event_loop()
    save_film = SaveFilm()
    to_do = [save_film(base_url, page_num, save_type='mysql') for page_num in range(500, 1000)]
    future = asyncio.wait(to_do)
    loop.run_until_complete(future)
    loop.close()


if __name__ == "__main__":
    cProfile.run('main()')

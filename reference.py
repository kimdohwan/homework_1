# 네이버 웹툰 크롤러 구현
# utils.py
#     클래스
#         Webtoon
#             기존 정보
#
#         Episode
#             webtoon <- webtoon_id대신 Webtoon인스턴스를 받도록 함
#             title
#             url
#
#         EpisodeImage
#             episode
#             url
#             file_path
#
# crawler.py
#     사용자 입력을 받아 처리해줌
#
# python crawler.py로 실행
# -----
#
# 안내) Ctrl+C로 종료합니다.
# 검색할 웹툰명을 입력해주세요: 대학
#  1. 대학일기
#  2. 안녕, 대학생
# 선택: 1
#
# 현재 "대학일기" 웹툰이 선택되어 있습니다
#  1. 웹툰 정보 보기
#  2. 웹툰 저장하기 (extra)
#  3. 다른 웹툰 검색해서 선택하기
# 선택: 1
#
#  대학일기
#     작가명: 자까
#     설명: 로망이 꽃피는 캠퍼스는 없다. 극사실주의에 기반한 너무나 현실적인 우리의 대학일기
#     총 연재회수:
#     등등...

from functions.game import *
from functions.shop import show_info as shop_info
from functions import shop
from friends.chat import send_message, send_message2

shop_info()

def turn_on():
    print('= Turn on game =')

    while True:
        choice = input('뭐할래?\n 1: 상점가기\n 2: 게임시작하기\n 3 or 4: 메시지 보내기\n 0: 종료\n  입력: ')
        if choice == '1':
            shop.buy_item()
        elif choice == '2':
            play_game()
        elif choice == '3':
            send_message()
        elif choice == '4':
            friend = input('친구명: ')
            message = input('메시지: ')
            send_message2(friend, message)
        elif choice == '0':
            break
        else:
            print('1, 2, 3중 하나를 입력해주세요')

if __name__ == '__main__':
    turn_on()

    ----------------------------------------------------------

from urllib import parse

import requests
import os.path

from bs4 import BeautifulSoup


class Episode:
    def __init__(self, webtoon_id, title, created_date, rating, no, url_thumbnail):
        self.webtoon_id = webtoon_id
        self.no = no
        self.url_thumbnail = url_thumbnail
        self.title = title
        self.rating = rating
        self.created_date = created_date

    @property
    def url(self):
        url_first_half = 'https://comic.naver.com/webtoon/detail.nhn?'
        params = {
            'titleId': self.webtoon_id,
            'no': self.no,
        }
        url = url_first_half + parse.urlencode(params)
        return url

    def episode_image_list(self):
        file_path = 'episode/episode-{}-{}.html'.format(self.webtoon_id, self.no)
        episode_url = self.url

        if os.path.exists(file_path):
            episode_html = open(file_path, 'rt').read()
        else:
            dir_path = 'episode'
            os.makedirs(dir_path, exist_ok=True)
            response = requests.get(episode_url)

            episode_html = response.text
            open(file_path, 'wt').write(episode_html)

        soup = BeautifulSoup(episode_html, 'lxml')

        img_url_list = soup.select('div.wt_viewer > img')
        # print(img_url_list)

        img_list = []
        for img in img_url_list:
            img_list.append(img.get('src'))
        return img_list


class Webtoon:
    def __init__(self, webtoon_id):
        self.webtoon_id = webtoon_id
        self._html = ''
        self._title = None
        self._author = None
        self._description = None
        self._episode_list = list()

    @property
    def html(self):
        if not self._html:
            url_webtoon_page = 'https://comic.naver.com/webtoon/list.nhn'
            params = {
                'titleId': self.webtoon_id,
            }
            file_path = 'webtoon_html/webtoonpage-{}.html'.format(self.webtoon_id)

            if os.path.exists(file_path):
                html_text = open(file_path, 'rt').read()
            else:
                response = requests.get(url_webtoon_page, params)
                html_text = response.text
                open(file_path, 'wt').write(html_text)
            self._html = html_text
        return self._html

    def set_info(self):
        soup = BeautifulSoup(self._html, 'lxml')

        div_detail = soup.select_one('div.detail > h2')
        title = div_detail.contents[0].strip()
        author = div_detail.contents[2].get_text(strip=True)
        description = soup.select_one('div.detail > p').get_text(strip=True)

        self._title = title
        self._author = author
        self._description = description

    @property
    def title(self):
        return self._get_info('_title')

    @property
    def author(self):
        return self._author

    @property
    def description(self):
        return self._description

    def _get_info(self, attr_name):
        if not getattr(self, attr_name):
            self.set_info()
        return getattr(self, attr_name)

    @property
    def episode_list(self):
        if not self._episode_list:
            soup = BeautifulSoup(self._html, 'lxml')

            table = soup.select_one('table.viewList')
            tr_all = table.select('tr')

            episode_list = list()
            for tr_num, tr in enumerate(tr_all[1:]):
                title = tr.select_one('td.title > a').get_text(strip=True)
                created_date = tr.select_one('td.num').get_text(strip=True)
                rating = tr.select_one('td strong').get_text(strip=True)

                url_thumbnail = tr.select_one('td:nth-of-type(1) > a').get('href')
                query_string = parse.urlsplit(url_thumbnail).query
                query_dict = parse.parse_qs(query_string)

                no = query_dict['no'][0]
                new_episode = Episode(self.webtoon_id, title, created_date, rating, no, url_thumbnail)
                episode_list.append(new_episode)
            self._episode_list = episode_list
        return self._episode_list
    # @property
    # def episode_list(self):
    #     if not self._episode_list:
    #         self.crawl_episode_list()
    #     return self._episode_list



if __name__ == '__main__':
    web = Webtoon(651673)
    web.html
    print(web.title)
    print(web.author)
    print(web.description)
    # print(web.episode_list)
    e1 = web.episode_list[0]
    print(e1.episode_image_list())

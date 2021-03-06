import os
from urllib import parse

import requests
from bs4 import BeautifulSoup


class Episode:
    def __init__(self, webtoon_id, title, created_date, rating, no, url_thumbnail):
        self.webtoon_id = webtoon_id
        self.title = title
        self.created_date = created_date
        self.rating = rating
        self.no = no
        self.url_thumbnail = url_thumbnail

    @property
    def url(self):
        url_first_half = 'https://comic.naver.com/webtoon/detail.nhn?'
        params = {
            'titleId': self.webtoon_id,
            'no': self.no,
        }
        url = url_first_half + parse.urlencode(params)
        return url

    def image_list(self):
        file_path = 'episode/episode-{}-{}.html'.format(self.webtoon_id, self.no)
        episode_url = self.url

        if os.path.exists(file_path):
            img_html = open(file_path, 'rt').read()
        else:
            dir_path = 'episode'
            os.makedirs(dir_path, exist_ok=True)

            response = requests.get(episode_url)
            img_html = response.text
            open(file_path, 'wt').write(img_html)

        soup = BeautifulSoup(img_html, 'lxml')

        img_container = soup.select('div.wt_viewer > img')

        image_list = []
        for img in img_container:
            img.get('src')
            image_list.append(img.get('src'))
        return image_list


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

            url_webtoon_page = 'http://comic.naver.com/webtoon/list.nhn'
            params = {
                'titleId': self.webtoon_id,
            }
            file_path = 'html-data/{}.html'.format(self.webtoon_id)

            if os.path.exists(file_path):
                html_text = open(file_path, 'rt').read()

            else:
                dir_path = 'html-data'
                os.makedirs(dir_path, exist_ok=True)

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
        return self._get_info('_author')

    @property
    def description(self):
        return self._get_info('_description')

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
                if tr.get('class'):
                    continue

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


if __name__ == '__main__':
    toon = Webtoon(703838)
    # toon.html
    print(toon.title)
    # e1 = toon.episode_list[0]
    # print(os.path.dirname(os.path.abspath(__file__)))
    # print(e1.no)
    # print(toon._title)
    # print(toon._description)
    # print(e1.no)
    # print(toon.episode_list)
    # print(e1.url)

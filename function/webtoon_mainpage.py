import os

import requests
from bs4 import BeautifulSoup


def crawl_mainpage():
    file_path = 'mainpage/main.html'
    url_main = 'https://comic.naver.com/webtoon/weekday.nhn'
    if os.path.exists(file_path):
        return open(file_path, 'rt').read()
    else:
        dir_path = f'{os.path.dirname(os.path.abspath(__file__))}/mainpage'
        os.makedirs(dir_path, exist_ok=True)

        response = requests.get(url_main)
        html = response.text
        open(file_path, 'wt').write(html)
        return html


def get_title():
    soup = BeautifulSoup(crawl_mainpage(), 'lxml')

    title_container_list = soup.select('div.col_inner li > a')

    title_list = []
    for title in title_container_list:
        title = title.get_text(strip=True)
        title_list.append(title)
    return title_list

if __name__ == '__main__':
    print(get_title()[1])
    print(os.path.dirname(os.path.abspath(__file__)))
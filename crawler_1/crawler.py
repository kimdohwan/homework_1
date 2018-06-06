from bs4 import BeautifulSoup
import requests
import os
from urllib import parse

# 1. 웹툰으로 이름 검색하기
url_webtoon_list = 'https://comic.naver.com/webtoon/weekday.nhn'

dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
# print(dir_path)

# html데이터를 미리 파일로 저장, 없으면 다운로드하고 있으면 해당내용 가져오기
file_path = os.path.join(dir_path, 'webtoon_list.html')
# print(file_path)

if os.path.exists(file_path):
    f = open(file_path, 'rt')
    html = f.read()
    f.close()
else:
    # 데이터를 보관할 파일을 생성
    os.makedirs(dir_path, exist_ok=True)

    # 웹툰 목록 url로부터 텍스트 데이터를 받아와서 html변수에 할당하기
    response = requests.get(url_webtoon_list)
    html = response.text
    f = open(file_path, 'wt')
    f.write(html)
    f.close()
    print('파일 쓰기 완료')

soup = BeautifulSoup(html, 'lxml')

# a태그인데 class가 title인 요소를 가져온다
a_list = soup.select('a.title')
# print(a_list)

# Get titles of webtoon from a tag(a_list)
title_list = []
for string in a_list:
    title = string.get_text(strip=True)
    title_list.append(title)
# print(title_list)

# Remove duplication of title in (title_list) using 'set' function
# print(len(title_list))
title_list = set(title_list)
# print(len(title_list))

# Create empty list(search_result_list) to restore result of search
# Take search word from user(input)
# Add webtoon title to list(search_result_list)
search_result_list = []
search_word = input('검색할 웹툰 제목을 입력하세요: ')
for title in title_list:
    if search_word in title:
        search_result_list.append(title)

# Print search result using index(enumerate)
for index, title in enumerate(search_result_list):
    print(f'{index+1}. {title}')

user_choice_webtoon = input('웹툰을 선택해주세요: ')

if user_choice_webtoon == '1':
    print('1. 웹툰정보 보기\n2. 이미지 다운로드')




# a요소들을 출력해본다
# a_text_list = []
# for a in a_list:
#     a_text_list.append(a.string)

# a_text_list = [a.string for a in a_list]

# 리스트 중복제거를 하는 원리(즐겨찾기 봐라)
# s = '21323113'
# result = dict.fromkeys(s)
# print(result)
# n = {1: '3'}
# m = list(n)
# print(m)
# 제목들의 리스트인 a_text_list의 중복을 없애준다
# a_text_list_set = set(a_text_list)
# a_text_list = list(a_text_list_set)

# search_result_list = []
# for a_text in a_text_list:
#     if '대학' in a_text:
#         print(a_text)
#         search_result_list.append(a_text)
# print(search_result_list)

# list comprehension으로 출력하는 방법
# t = []
# t = [univ for univ in a_text_list if '대학' in univ]
# print(t)

# a_dict = []
# for a in a_list:
#     href = a.get('href')
#     query_dict = parse.parse_qs(parse.urlsplit(href).query)
#     webtoon_id = query_dict.get('titleId')[0]


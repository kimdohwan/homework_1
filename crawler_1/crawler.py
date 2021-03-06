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

# Bring id, title from a tag
# Create list and make list element to dict type having id,title
title_id_dict = []
for a in a_list:
    href = a.get('href')
    urlsplit = parse.urlsplit(href)
    query = urlsplit.query
    query_set = parse.parse_qs(query)
    title_id = query_set['titleId'][0]
    title = a.string

    title_id_dict.append({
        'titleId': title_id,
        'title': title
    })
# print(len(title_id_dict))

# There is some duplication in (title_id_dict)
# Using 'set()', 'continue' in 'if', remove duplication
webtoon_id_set = set()
title_id_dict = []
for a in a_list:
    href = a.get('href')
    urlsplit = parse.urlsplit(href)
    query = urlsplit.query
    query_set = parse.parse_qs(query)
    title_id = query_set['titleId'][0]
    title = a.string

    if title_id in webtoon_id_set:
        continue
    webtoon_id_set.add(title_id)
    title_id_dict.append({
        'titleId': title_id,
        'title': title
    })
# print(len(title_id_dict))
# print(title_id_dict)


# -----------------------------검색---------------------------------

# Create empty list(search_result_list) to restore result of search
# Take search word from user(input)
# Add webtoon title to list(search_result_list)
while True:
    search_result_list = []
    user_search_word = input('검색할 웹툰 제목을 입력하세요: ')
    for title in title_list:
        if user_search_word in title:
            search_result_list.append(title)

    # Print search result using index(enumerate)
    for index, title in enumerate(search_result_list):
        print(f'{index+1}. {title}')

    if not search_result_list:
        print(f'웹툰 {user_search_word}가 존재하지 않습니다')
        continue
    else:
        pass

    user_choice_webtoon_num = input('웹툰 번호를 선택해주세요: ')

    # (result) get title which user choice using 'enumerate' and 'index'
    for index, title in enumerate(search_result_list):
        if user_choice_webtoon_num == f'{index+1}':
            result = title
    # print(result)

    # Match (result) with ['title'] of (title_id_dict)
    # Get titleid from (title_id_dict)
    selected_webtoon_id = ''
    for search_title in title_id_dict:
        if result == search_title['title']:
            t = search_title['title']
            selected_webtoon_id = search_title['titleId']
            print(f'\n웹툰 [{t}]이/가 선택되었습니다')

    while True:

        user_choice_detail = input(' 1. 웹툰 정보 보기\n 2. 웹툰 저장하기\n 3. 다른 웹툰 검색하기\n')
        # print(selected_webtoon_id)

        if user_choice_detail == '1':
            print(f'웹툰 정보보기 선택')
            dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
            # print(dir_path)
            file_path = os.path.join(dir_path, f'{selected_webtoon_id}.html')
            # print(file_path)
            url = 'https://comic.naver.com/webtoon/list.nhn?titleId={}'.format(selected_webtoon_id)
            # print(url)

            if os.path.exists(file_path):
                f = open(file_path, 'rt')
                html = f.read()
                f.close()
                print('html 파일이 이미 존재하여 읽기 실행\n')

            else:
                response = requests.get(url)
                html = response.text
                f = open(file_path, 'wt')
                f.write(html)
                f.close()
                print('html파일 새로 받아 저장 완료\n')

            soup = BeautifulSoup(html, 'lxml')
            # print(soup)

            # 제목, 설명, 작가
            h2 = soup.select_one('div.detail > h2')
            # print(type(div_container))
            title = h2.contents[0].strip()
            print(f'웹툰 정보\n 제목: {title}')
            author = h2.contents[1].get_text(strip=True)
            print(f' 작가: {author}')
            description = soup.select_one('div.detail > p').string
            u = input(f' 줄거리: {description}\n 2. 웹툰 저장 3.다른 웹툰 보기')
            if u == '2':
                pass
            elif u == '3':
                break

        if user_choice_detail == '2':
            print('웹툰 다운로드')
            break

        elif user_choice_detail == '3':
            break


#
# a요소들을 출력해본다
# a_text_list = []
# for a in a_list:
#     a_text_list.append(a.string)
#
# a_text_list = [a.string for a in a_list]
#
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
#
# search_result_list = []
# for a_text in a_text_list:
#     if '대학' in a_text:
#         print(a_text)
#         search_result_list.append(a_text)
# print(search_result_list)
#
# list comprehension으로 출력하는 방법
# t = []
# t = [univ for univ in a_text_list if '대학' in univ]
# print(t)
#
# a_dict = []
# for a in a_list:
#     href = a.get('href')
#     query_dict = parse.parse_qs(parse.urlsplit(href).query)
#     webtoon_id = query_dict.get('titleId')[0]
#

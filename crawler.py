from function.webtoon_crawling import *
from function.webtoon_mainpage import *


# def page_one():
#     if choice == '1':
#         input(f" 현재 '{toon.title}'에 선택되어 있습니다.\n 1: 웹툰 정보 보기\n 2: 웹툰 저장하기\n 3: 다른 웹툰 검색해서 선택하기\n 입력: ")
#         if choice == '1':
#             print(f' 작가: {toon.author}\n 설명: {toon.description}\n 총 회수: {e1.no}')
#         elif choice == '3':
#             page_one()

def turn_on():
    print('Crtl+C로 종료합니다')
    while True:
        print('검색할 웹툰명을 입력해주세요:')
        choice = input('')

        search_result = []
        for index, i in enumerate(get_title()):
            if choice in get_title()[index]:
                search_result.append(get_title()[index])
        for index, title in enumerate(search_result):
            print(f'{index+1}: {title}\n')
        choice = input('웹툰을 선택해주세요 ex)1\n 선택:')

        input(f" 현재 '{search_result[choice-1]}'에 선택되어 있습니다.\n 1: 웹툰 정보 보기\n 2: 웹툰 저장하기\n 3: 다른 웹툰 검색해서 선택하기\n 입력: ")
            #
            # if choice == '1':
            #     print(f' 작가: {toon.author}\n '
            #           f'설명: {toon.description}\n '
            #           f'총 회수: {e1.no}')
            # elif choice == '3':
            #     continue





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



# print(e1.image_list())

if __name__ == '__main__':
    turn_on()

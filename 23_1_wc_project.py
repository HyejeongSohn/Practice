import requests
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from collections import Counter
from konlpy.tag import Okt
from wordcloud import WordCloud
import tkinter as tk
from tkcalendar import Calendar

stopwords = ['있다', '하는', '그', '이', '저', '것', '수', '등', '들', '를','좀', '잘', '더', '더욱', '많이', '매우', '정말', '진짜', '너무', '아주',
                          '안', '로', '에서', '에', '과', '와', '한', '하다', '입니다', '입니다', '입니다','하고', '한다', '하는', '그리고', '그런', '이런', '저런', 
                          '할', '합니다', '했습니다','합니다', '했었습니다', '있는', '있었습니다', '하는', '하는데', '한다고', '하면', '한다면', '기자', '제공', '무단', 
                          '배포', '무단배포', '배포금지', '이번', '위해', '라며', '금지', '뉴스', '통해', '오늘', '지난달', '지난', '대한', '경우', '관련', '뉴시스', 
                          '현재', '이유', '단독', '논란', '지난해', '때문', '지금', '또한', '만큼', '최근', '당시', '올해', '대해', '다시', '모두', '왜', '또']



def get_news_titles(start_date, end_date=None):
    news_titles = []  # 뉴스 제목을 저장할 리스트
    date_range = pd.date_range(start=start_date, end=end_date) if end_date else [
        start_date]  # 시작 날짜와 종료 날짜 사이의 모든 날짜를 포함하는 리스트 생성

    twitter = Okt()  # 형태소 분석기 객체 생성

    for date in date_range:  # 각 날짜에 대해 반복
        url = 'https://news.naver.com/main/ranking/popularDay.nhn?date={}'.format(
            date.strftime('%Y%m%d'))  # 해당 날짜의 뉴스 랭킹 페이지 URL 생성

        headers = {
            'User-Agent': 
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
        req = requests.get(url, headers=headers)  # URL로 요청 보내기
        soup = BeautifulSoup(req.text, 'html.parser')  # 응답의 HTML 파싱
        titles = soup.select('.rankingnews_box > ul > li > div > a')  # 뉴스 제목 선택
        for title in titles:  # 각 뉴스 제목에 대해 반복
            nouns = twitter.nouns(title.text)  # 제목에서 명사 추출
            filtered_nouns = [noun for noun in nouns if noun not in stopwords]  # 불용어 제거
            # 추출한 명사들을 뉴스 제목 리스트에 추가
            news_titles.extend(filtered_nouns)

    return news_titles

def generate_wordcloud(text):
    count = Counter(text)  # 단어 빈도수 계산

    wc = WordCloud(font_path=r'C:\Windows\Fonts\NanumGothic.ttf',
                   background_color='white', width=800, height=600)
    cloud = wc.generate_from_frequencies(count)  # 빈도수에 따라 워드 클라우드 생성

    return cloud

def show_calendar(entry): # 달력 표시하기
    # 달력에서 날짜를 선택하면 해당 날짜를 엔트리에 입력하는 함수
    def set_date():
        entry.delete(0, tk.END) # entry의 내용 삭제
        entry.insert(0, cal.selection_get().strftime(
            '%Y-%m-%d')) # 달력에서 선택한 날짜를 entry에 삽입
        top.destroy() # 윈도우 창 닫기

    # 새로운 창에서 달력 보여주기
    top = tk.Toplevel(root)
    cal = Calendar(top, font="Arial 14", selectmode='day', locale='en_US', cursor='hand1')
    cal.pack(fill='both', expand=True)

    btn_ok = tk.Button(top, text="OK", command=set_date)
    btn_ok.pack()

def option_radio_click():
    if option_var.get() == "날짜 구간 지정하기":
        end_label.grid(row=2, column=0)
        end_date_entry.grid(row=2, column=1)
        end_calendar_button.grid(row=2, column=2)
    else:
        end_label.grid_remove()
        end_date_entry.grid_remove()
        end_calendar_button.grid_remove()

# 워드 클라우드를 보여주는 함수
def show_wordcloud():
    option = option_var.get()
    site = site_var.get()

    if option == "한 날짜 보기":
        start_date = start_date_entry.get()
        end_date = start_date
    else:
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()

    news_titles = get_news_titles(start_date, end_date)
    cloud = generate_wordcloud(news_titles)

    plt.figure(figsize=(10, 8))
    plt.imshow(cloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

# tkinter를 이용한 GUI 창 생성
root = tk.Tk()
root.title("뉴스 워드 클라우드")

# 날짜 선택 옵션 라벨과 라디오 버튼 생성
option_label = tk.Label(root, text="날짜 선택 옵션:")
option_label.grid(row=0, column=0)

option_var = tk.StringVar()
option_var.set("한 날짜 보기") # 기본 옵션 설정

option_radio1 = tk.Radiobutton(root, text="한 날짜 보기", variable=option_var, value="한 날짜 보기", command=option_radio_click)
option_radio1.grid(row=0, column=1)

option_radio2 = tk.Radiobutton(root, text="날짜 구간 지정하기", variable=option_var, value="날짜 구간 지정하기", command=option_radio_click)
option_radio2.grid(row=0, column=2)

# 시작 날짜 입력 엔트리와 달력 버튼 생성
start_label = tk.Label(root, text="시작 날짜:")
start_label.grid(row=1, column=0)

start_date_entry = tk.Entry(root)
start_date_entry.grid(row=1, column=1)

start_calendar_button = tk.Button(root, text="달력", command=lambda: show_calendar(start_date_entry))
start_calendar_button.grid(row=1, column=2)

# 종료 날짜 입력 엔트리와 달력 버튼 생성
end_label = tk.Label(root, text="종료 날짜:")
end_label.grid(row=2, column=0)

end_date_entry = tk.Entry(root)
end_date_entry.grid(row=2, column=1)

end_calendar_button = tk.Button(root, text="달력", command=lambda: show_calendar(end_date_entry))
end_calendar_button.grid(row=2, column=2)

# 숨기기

end_label.grid_remove()
end_date_entry.grid_remove()
end_calendar_button.grid_remove()

# 사이트 선택 라벨과 라디오 버튼 생성
site_label = tk.Label(root, text="사이트 선택:")
site_label.grid(row=3, column=0)

site_var = tk.StringVar()
site_var.set("많이 본 뉴스 보기") # 기본 사이트 설정

site_radio1 = tk.Radiobutton(root, text="많이 본 뉴스 보기", variable=site_var, value="많이 본 뉴스 보기")
site_radio1.grid(row=3, column=1)

site_radio2 = tk.Radiobutton(root, text="댓글 많은 뉴스 보기", variable=site_var, value="댓글 많은 뉴스 보기")
site_radio2.grid(row=3, column=2)

site_radio3 = tk.Radiobutton(root, text="둘 다 보기", variable=site_var, value="둘 다 보기")
site_radio3.grid(row=4, column=1, columnspan=2)

# 워드 클라우드 보기 버튼 생성
show_wordcloud_button = tk.Button(root, text="워드 클라우드 보기", command=show_wordcloud)
show_wordcloud_button.grid(row=5, column=1, pady=10)

root.mainloop()

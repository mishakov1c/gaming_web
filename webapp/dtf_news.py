from datetime import datetime

import requests
from bs4 import BeautifulSoup

from webapp.model import db, Articles

def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print("Сетевая ошибка")
        return False
    
def get_dtf_news():
    html = get_html("https://dtf.ru/")
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_news = soup.findAll('div', class_ = 'feed__item')
        result_news = []
        for news in all_news:
            title = news.find('div', class_ = 'content-title')
            try:
                title = title.text.replace("Статьи редакции", "").strip()
                # print(title)
            except AttributeError:
                continue
            url = news.find('a', class_ = 'content-link')['href']
            written = news.find('time', class_ = 'time')['title']
            written = written[:11].strip()
            try:
                written = datetime.strptime(written, '%d.%m.%Y')
            except ValueError:
                written = datetime.now()        
            save_news(title, url, written) 

def save_news(title, url, written):
    news_exists = Articles.query.filter(Articles.url == url).count()
    if not news_exists:
        new_articles = Articles(title=title, url=url, written=written, author='unknown', is_published = 1)
        db.session.add(new_articles)
        db.session.commit()    

# if __name__ == "__main__":
#     news = get_dtf_news()
#     print(news)
import requests
from bs4 import BeautifulSoup

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
                print(title)
            except AttributeError:
                continue

            url = news.find('a', class_ = 'content-link')['href']
            written = news.find('time', class_ = 'time')['title']
            written = written[:11].strip().replace('.', '/')
            result_news.append({
                "title": title,
                "url": url,
                "written": written    
            }) 
        return result_news  
    return False  

    
if __name__ == "__main__":
    news = get_dtf_news()
    print(news)
"""
Most Popular Post on detik.com - Scraper
"""

# 1.Import Python libraries used for web scraping
import requests
from bs4 import BeautifulSoup


# 2.Extracting data from targeted site
def data_extraction():
    """
    #1 First Article
    #2 Second Article
    #3 Third Article
    #4 Fourth Article
    #5 Fifth Article
    :return:
    """
    try:
        content = requests.get("https://www.detik.com/")
    except Exception:
        return None
    if content.status_code == 200:
        soup = BeautifulSoup(content.text, 'html.parser')
        list_content = soup.find('div', {'class': 'box cb-mostpop'})
        list_content = list_content.find('div', {'class': 'list-content'})

        num_list = list_content.find_all('span', {'class': 'text-list__data'})
        popular_post_list = list_content.find_all('a', {'class': 'media__link'})
        category_date_list = list_content.find_all('div', {'class': 'media__date'})
        category_list = []
        date_list = []

        for div in category_date_list:
            category, date = div.text.split(' | ')
            category_list.append(category)
            date_list.append(date)

        news_list = []
        for n, p, t, l in zip(num_list, popular_post_list, category_list, date_list):
            news = f'{n.text.strip()} {p.text.strip()} - {t.strip()} |{l.strip()}'
            news_list.append(news)
        result = '\n'.join(news_list)

        return news_list
    else:
        return None


# 3.Showing extracted result
def result_display(result):
    if result is None:
        print("can't display the data")
        return
    for news_item in result:
        print(news_item)

# 4.If Executed as Stand-Alone Program
if __name__ == '__main__':
    print('Main Apps')
    result = data_extraction()
    result_display(result)
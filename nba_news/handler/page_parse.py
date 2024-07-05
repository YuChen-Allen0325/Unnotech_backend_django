import requests
import copy
from bs4 import BeautifulSoup


def Bs4Soup(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    return soup


def SearchLastPage(first_page_url):

    soup = Bs4Soup(first_page_url)

    gonext = soup.find('gonext').find_all('a')
    last_page_url = gonext[-1].get('href')
    first_slash_from_bottom = last_page_url.rfind('/')
    max_page_number = int(last_page_url[(first_slash_from_bottom + 1):])

    return max_page_number


def MutableMainbar(url):

    soup = Bs4Soup(url)

    news_list_body = soup.find('div', id='news_list_body')
    dts = news_list_body.find('dl').find_all('dt')

    tmp = {}
    stored_data = []
    filter_db_data = []

    for dt in dts:
        detail_url = dt.find('a').get('href')
        img_url = dt.find('img', class_="lazyload").get('data-src')
        title = dt.find('h3').get_text()
        datetime = dt.find('b', class_="h24").get_text()
        paragraph = dt.find('p').get_text()

        tmp['detail_url'] = detail_url
        tmp['img_url'] = img_url
        tmp['title'] = title
        tmp['datetime'] = datetime
        tmp['paragraph'] = paragraph

        copied_tmp = copy.deepcopy(tmp)
        stored_data.append(copied_tmp)
        filter_db_data.append(detail_url)    # 內容頁的URL作為判斷新聞是否有更新

    return stored_data, filter_db_data


def DetailPageInfo(detail_url):

    soup = Bs4Soup(detail_url)

    story_body_content = soup.find('div', id="story_body_content")
    detail_title = story_body_content.find('h1').get_text()
    author = story_body_content.find(
        'div', class_="shareBar__info--author").get_text()
    span = story_body_content.find_all('span')
    paragraph = ''

    for i in span:
        paragraph += str(i)
        paragraph += '\n'

    return [{"detail_title": detail_title, "author": author, "paragraph": paragraph}]


def SidebarInfo(url):

    soup = Bs4Soup(url)

    hot_articles_body = soup.find('div', id="hot_articles_body")
    sidebar_title = hot_articles_body.find_all('dl')

    sidebar = ''

    for i in sidebar_title:
        sidebar = str(i.get_text()).replace('\n\n', ' ').replace(' ', '')
        sidebar = sidebar.split('\n')

    return sidebar

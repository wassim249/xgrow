import os

import bs4
import requests
from selenium import webdriver
from selenium.webdriver.firefox.service import Service


def load_posted_news(username: str)->list[str]:
    """
    Description:
    This function is responsible for loading the posted news for a user.
    Args:
        username (str): The username of the user.
    Returns:
        list: The list of posted news.
    """
    try:
        with open(f"data/posted_news/{username}.txt", "r") as f:
            return f.read().splitlines()
    except FileNotFoundError:
        return []


def save_posted_news(username: str, posted_news: str)->None:
    """
    Description:
    This function is responsible for saving the posted news for a user.
    Args:
        username (str): The username of the user.
        posted_news (str): The posted news content.
    """
    if not os.path.exists("data/posted_news"):
        os.makedirs("data/posted_news",exist_ok=True)
    with open(f"data/posted_news/{username}.txt", "a") as f:
        f.write(f"{posted_news}\n")


def fetch_news(username: str)->list[dict]:
    """
    Description:
    This function is responsible for fetching news from the web.
    Args:
        username (str): The username of the user.
    Returns:
        list: The list of news fetched from the web.
    """
    url = "https://www.artificialintelligence-news.com/"

    # read url content
    page = requests.get(url)
    # get only the body content
    soup = bs4.BeautifulSoup(page.content, 'html.parser')

    featured_news = soup.find_all('div', {'class': 'cell blocks small-12 medium-3 large-3'})
    posted_news = load_posted_news(username)
    news = []
    for news_item in featured_news:
        title = news_item.find('h3').find('a').text
        if title in posted_news:
            continue
        news.append({
            "title": title,
            "link": news_item.find('h3').find('a')['href']
        })

    if not news:
        return []

    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options, service=Service("./driver/geckodriver"))

    for news_item in news:
        driver.get(news_item['link'])
        soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')

        news_item['content'] = soup.find('article', {'data-title': news_item['title']}).find_all('p')[1:-5]
        # remove double spaces
        news_item['content'] = ' '.join([p.text for p in news_item['content']]).replace('  ', ' ')

        # remove special characters
        news_item['content'] = ''.join(e for e in news_item['content'] if e.isalnum() or e.isspace())
        # remove \n
        news_item['content'] = news_item['content'].replace('\n', ' ')

        # trim to 1000 characters
        news_item['content'] = news_item['content'][:1000]

    return news

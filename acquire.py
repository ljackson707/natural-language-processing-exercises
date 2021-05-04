from requests import get
import requests
from bs4 import BeautifulSoup
import pandas as pd

#-------------------------------------------------------------------------------------------------------------------------------

def process_article(article):
    title = article.find('h2').text
    date_and_byline_div = article.select('.grid.grid-cols-2.italic')[0]
    date_p, by_p = date_and_byline_div.find_all('p')
    summary = article.find_all('p')[-1].text
    
    return {
        "title": title,
        "date": date_p.text,
        "by": by_p.text,
        "summary": summary
    }

#-------------------------------------------------------------------------------------------------------------------------------

def get_codeup_blog(url):

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"}
    response = get(url, headers = headers)
    
    soup = BeautifulSoup(response.text)
    
    # Title
    Title = soup.select('h1.jupiterx-post-title')[0].text

    # Body
    Content = soup.select('.jupiterx-post-content')[0].text

    # Time
    Time = soup.time.text
    
    output = {}
    output['Title'] = Title
    output['Time'] = Time
    output['Content'] = Content
    
    return output

#-------------------------------------------------------------------------------------------------------------------------------

def get_blog_articals(urls):
    posts = [get_codeup_blog(url) for url in urls]
    
    return pd.DataFrame(posts)

#-------------------------------------------------------------------------------------------------------------------------------

def get_article(article, category):
    # Attribute selector
    title = article.select("[itemprop='headline']")[0].text
    
    # article body
    content = article.select("[itemprop='articleBody']")[0].text
    
    output = {}
    output["title"] = title
    output["content"] = content
    output["category"] = category
    
    return output

#-------------------------------------------------------------------------------------------------------------------------------

def get_articles(category):
    """
    This function takes in a category as a string. Category must be an available category in inshorts
    Returns a list of dictionaries where each dictionary represents a single inshort article
    """
    base = "https://inshorts.com/en/read/"
    
    # We concatenate our base_url with the category
    url = base + category
    
    # Set the headers to show as Netscape Navigator on Windows 98, b/c I feel like creating an anomaly in the logs
    headers = {"User-Agent": "Mozilla/4.5 (compatible; HTTrack 3.0x; Windows 98)"}

    # Get the http response object from the server
    response = get(url, headers=headers)

    # Make soup out of the raw html
    soup = BeautifulSoup(response.text)
    
    # Ignore everything, focusing only on the news cards
    articles = soup.select(".news-card")
    
    output = []
    
    # Iterate through every article tag/soup 
    for article in articles:
        
        # Returns a dictionary of the article's title, body, and category
        article_data = get_article(article, category) 
        
        # Append the dictionary to the list
        output.append(article_data)
    
    # Return the list of dictionaries
    return output

#-------------------------------------------------------------------------------------------------------------------------------

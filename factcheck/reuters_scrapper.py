# pip install semanticscholar
# pip install newspaper3k
# pip install summa
# pip install pattern
from bs4 import BeautifulSoup
import requests
import urllib.request,sys,time
import re
import pandas as pd
from newspaper import Article
import json
#from summa import keywords
import nltk
import pattern as patt
from semanticscholar import SemanticScholar
import htmlmin  

def requestpage(URL):
    try:

        # this might throw an exception if something goes wrong.
        page=requests.get(URL) 
        # this describes what to do if an exception is thrown 
    except Exception as e:    
  
        # get the exception information
        error_type, error_obj, error_info = sys.exc_info()      
        
        #print the link that cause the problem
        print ('ERROR FOR LINK:', URL)
        
        #print error info and line that threw the exception                          
        print (error_type, 'Line:', error_info.tb_lineno)
    return page

list_articles_url = []


count = 1
article_count = 0
while len(list_articles_url) < 2230:

    URL = 'https://www.reuters.com/news/archive/factchecknew?view=page&page='+str(count)+'&pageSize=10'
    count += 1
    page = requestpage(URL)
    soup = BeautifulSoup(page.text, "html.parser")
    
    
    if len(soup.find_all(attrs={'class': 'news-headline-list'})) == 0:
        break

    articles_archives = soup.find_all(attrs={'class': 'news-headline-list'})[0]

    articles = articles_archives.find_all('article')

    for article in articles:
        a_tag = article.find('a')

        if a_tag.attrs['href'] not in list_articles_url:
            list_articles_url.append({ 'url' : a_tag.attrs['href']})
            article_count += 1
    if article_count % 100 == 0:
        print(article_count, " articles extracted so far")


print(len(list_articles_url))
print("end of first loop")
reuters_data_list = []

count = 0

for item in list_articles_url:
    try:
        url = 'https://www.reuters.com/news' + item['url']
        page = requestpage(url)
        soup = BeautifulSoup(page.text, "html.parser")
        title = soup.find("meta", {'property':'og:title'}).attrs['content']
        claim = soup.find("meta", {'property':'og:description'}).attrs['content']
        time = soup.find("meta", {'property':'og:article:published_time'}).attrs['content']

        # scrape all links
        all_links = []
        href_tags = soup.find_all(href=True)
        for tag in href_tags:
            href = tag.get('href')
            if href[0] == '/':
                href = url + href
            all_links.append(href)

        data = ''
        content = ""
        for data in soup.find_all('p'):
            content += data.get_text()

        #print()

        reuters_data = {
            'title': title[11:],
            'claim': claim,
            'time': time,
            'url': url,
            'plaintext': content[10:],
            'all_links':all_links,
        }

        if reuters_data:
            #print(reuters_data,"\n")
            reuters_data_list.append(reuters_data)
            count += 1
            if count % 100 == 0:
                print(count, " articles done")

    except Exception as e:
        # get the exception information
        error_type, error_obj, error_info = sys.exc_info()      
        
        #print error info and line that threw the exception                          
        print (error_type, 'Line:', error_info.tb_lineno)
        print (e)


print("number of articles: ", count)
df_articles = pd.DataFrame(reuters_data_list)
df_articles.to_csv('reutersarticles.csv', encoding='utf-8-sig')

# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
from time import sleep
from tqdm import tqdm
import os

def getAllArticleURL():
    all_article_url = []
    base_url = 'https://medley.life'
    next_page_url = 'https://medley.life/news/'

    while True:
        article_url = []
        soup = crawler(next_page_url)
        article_codes = soup.find_all('li', class_ = 'o-news-article-list__item')
        for code in article_codes:
            # 記事のURLを取得
            url = base_url + code.find('a').get('href')
            # 記事URLリストに追加
            article_url.append(url)
        # 全記事URLリストに追加
        all_article_url.append(article_url)
        # 次のページを探す
        next_page_code = soup.find('a', class_ = 'o-pagination__next')
        # 次のページがない場合
        if next_page_code == None:
            break
        # 次のページがある場合
        else:
            # 次のページのURLを取得
            next_page_url = base_url + next_page_code.get('href')
        sleep(SLEEP_TIME)
    return all_article_url

def crawler(url):
    while True:
        page = requests.get(url)
        if page.status_code == 200:
            break
        else:
            print('クローリングに失敗しました')
            print('再度クローリングを行います')
            sleep(SLEEP_TIME)
    return BeautifulSoup(page.text, 'lxml')

def titleScraiper(soup):
    title = soup.find('h1', class_ = 'o-page-top__news_title').text.strip()
    return title

def contentScraiper(soup):
    content = ''
    for c in soup.find_all('div', class_ = 'o-item-content o-item-content-news'):
        content += c.get_text().strip()
        '''
        for p in c.find_all('p'):
            content += p.text.strip()
        for ul in c.find_all('ul'):
            for li in ul.find_all('li'):
                content += li.text.strip()
        '''
    content = content.replace('\n', '').replace(u'®', '')
    return content

def dateScraiper(soup):
    date = soup.find('p', class_ = 'o-page-top__news_date').text.strip().replace(u' ｜ ニュース', '').replace(u' ｜ PR', '')
    return date

def outputList(url, titles, length):
    # ファイルがない時新規
    if not os.path.exists('./articles_list.txt'):
        u = open('articles_list.txt', 'w')
    # ファイルがある時追加書き込み
    else:
        u = open('articles_list.txt', 'a')
    for i, title in enumerate(titles):
        u.write(title.encode('utf-8'))
        u.write('\n')
        u.write(url[i])
        if len(open('articles_list.txt').readlines()) != length * 2:
            u.write('\n')
    u.close()

def outputContent(contents, no):
    # ディレクトリがない時新規
    if not os.path.exists('./ARTICLES'):
        os.mkdir('ARTICLES')
    # ディレクトリに移動
    os.chdir('./ARTICLES')
    for content in contents:
        c = open(str(no) + '.txt', 'w')
        c.write(content.encode('utf-8'))
        c.close()
        no += 1
    os.chdir('../')

def outputDate(dates, length):
    # ファイルがない時新規
    if not os.path.exists('./articles_date.txt'):
        d = open('articles_date.txt', 'w')
    # ファイルがある時追加書き込み
    else:
        d = open('articles_date.txt', 'a')
    for i, date in enumerate(dates):
        d.write(date.encode('utf-8'))
        if len(open('articles_date.txt').readlines()) != length:
            d.write('\n')
    d.close()

def main():
    # 全ての記事のURLを取得
    print('各記事のURLを収集開始')
    all_article_url = getAllArticleURL()
    print(all_article_url)
    print('各記事のURLを収集完了')

    #各URLにアクセスし記事タイトルと内容を取得と保存
    article_no = 0
    for article_url in tqdm(all_article_url):
        titles = []
        contents = []
        dates = []
        # 取得
        for url in article_url:
            soup = crawler(url)
            titles.append(titleScraiper(soup))
            contents.append(contentScraiper(soup))
            dates.append(dateScraiper(soup))
        # 保存
        outputList(article_url, titles, len(all_article_url))
        outputContent(contents, article_no)
        outputDate(dates, len(all_article_url))
        # 番号を増やす
        article_no += len(article_url)

if __name__ == '__main__':
    SLEEP_TIME = 1
    main()

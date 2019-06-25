# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
from time import sleep
from tqdm import tqdm
import os

def getAllArticleURL():
    all_article_url = []
    base_url = 'https://doctors-me.com'
    next_page_url = 'https://doctors-me.com/doctor/column'
    base_page_url = 'https://doctors-me.com/doctor/column?page='

    # サイトのサーバーが不良のため，手入力で137ページを指定して記事を取得
    for i in range(138):
        next_page_url = base_page_url + str(i + 1)
        article_url = []
        soup = crawler(next_page_url)
        ul_tag = soup.find('ul', class_='list-feat')
        for li_tag in ul_tag.find_all('li'):
            # 記事のURLを取得
            if li_tag.find('div', class_='list-feat__image') != None:
                url = base_url + li_tag.find('a').get('href')
                # 記事URLリストに追加
                article_url.append(url)
        # 全記事URLリストに追加
        all_article_url.append(article_url)
        sleep(SLEEP_TIME)
    return all_article_url
    '''
    # 自動に収集する方法
    while True:
        article_url = []
        soup = crawler(next_page_url)
        ul_tag = soup.find('ul', class_ = 'list-feat')
        for li_tag in ul_tag.find_all('li'):
            # 記事のURLを取得
            if li_tag.find('div', class_ = 'list-feat__image') != None:
                url = base_url + li_tag.find('a').get('href')
                # 記事URLリストに追加
                article_url.append(url)
        # 全記事URLリストに追加
        all_article_url.append(article_url)
        # 次のページを探す
        next_page_code = soup.find('a', class_ = 'pagination__next')
        # 次のページがない場合
        if next_page_code == None:
            break
        # 次のページがある場合
        else:
            # 次のページのURLを取得
            next_page_url = base_url + next_page_code.get('href')
        sleep(SLEEP_TIME)
        '''
    '''
    soup = crawler(next_page_url)
    article_url = []
    soup = crawler(next_page_url)
    ul_tag = soup.find('ul', class_ = 'list-feat')
    for li_tag in ul_tag.find_all('li'):
        # 記事のURLを取得
        if li_tag.find('div', class_ = 'list-feat__image') != None:
            url = base_url + li_tag.find('a').get('href')
            # 記事URLリストに追加
            article_url.append(url)
    # 全記事URLリストに追加
    all_article_url.append(article_url)
    '''

'''
def getAllArticleURL(page_url):
    all_article_url = []
    base_url = 'https://medley.life'
    for url in page_url:
        soup = crawler(url)
        article_codes = soup.find_all('li', class_ = 'o-news-article-list__item')
        for code in article_codes:
            url = base_url + code.find('a').get('href')
            all_article_url.append(url)
            print(url)
        sleep(SLEEP_TIME)
    return all_article_url
'''

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
    title = soup.find('h1', class_ = 'column-title').get_text().strip()
    return title

def contentScraiper(soup):
    content_code = soup.find('div', class_ = 'post-content')
    # PRではない記事
    if content_code != None:
        content = content_code.text.strip()
    # PRの記事
    else:
        content = soup.find('div', class_ = 'post-detail').text.strip()

    content = content.replace('\n', '').replace(u' ', '').replace(u' ', '').replace(u'■', '').replace(u'・', '')\
        .replace(u'□', '').replace(u'※', '').replace(u'（※）', '').replace(u'目次', '').replace(u'(監修：DoctorsMe医師)', '')\
        .replace(u'　', '').replace(u'参考文献', '')
    return content

def dateScraiper(soup):
    date = soup.find('p', class_ = 'post-date').text.strip().replace(u'記事投稿日：', '').replace(u'記事更新日：', '').replace(u' ', '').replace('\n', '').replace('PR', '')
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
    SLEEP_TIME = 2
    main()

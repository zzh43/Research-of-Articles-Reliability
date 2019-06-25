# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from time import sleep
from selenium.common.exceptions import ElementNotVisibleException
from tqdm import tqdm
import os

def getFullHtml():
    # PhantomJSを起動
    driver = webdriver.PhantomJS()

    #指定したURLにアクセス
    url = 'https://style.nikkei.com/healthup'
    driver.get(url)

    # ページの下にあるボタンを押しページを展開
    while True:
        try:
            driver.find_element_by_css_selector('#conts > div.more > a').click()
            sleep(SLEEP_TIME)
        except ElementNotVisibleException:
            break

    # フールページのソースコードを保存
    full_html = driver.page_source

    # PhantomJSを停止
    driver.quit()

    return full_html

def getFullURL(html):
    soup = BeautifulSoup(html, 'lxml')
    full_url = []
    base_url = 'https://style.nikkei.com/'
    # 記事のURLを取得
    article_codes = soup.find_all('a', class_ = 'a-article')
    for code in article_codes:
        url = code.get('href')
        full_url.append(base_url + url)
    return full_url

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
    title = soup.find('p', class_ = 'text').text.strip().replace('\n', '').replace(' ', '').replace(u'　', '')
    return title

def contentScraiper(soup):
    next_pages = soup.find('ul', class_ = 'pagination_article_detail clearfix')
    # 記事は複数のページがある場合
    if next_pages is not None:
        content = ''
        next_page_urls = []
        # 現在のページ以外の全てのページのURLを取得
        for next_page in next_pages.find_all('a'):
            next_page_urls.append(next_page.get('href'))
        # 次へのURLを削除
        next_page_urls.pop()
        # 現在のページの内容を読み取る
        content += contentReader(soup)
        # 他のページの内容を読み取る
        for next_page_url in next_page_urls:
            soup = crawler(next_page_url)
            content += contentReader(soup)
            sleep(SLEEP_TIME)
    else:
        content = contentReader(soup)
    content = content.replace('\n', '').replace('\r', '').replace('\r\n', '')
    return content

def contentReader(soup):
    content = ''
    c = soup.find('div', class_ = 'text01')
    for p in c.find_all('p'):
        if p.find('span', class_ = 'cmn-editable_bold'):
            # 記事内の大文字の部分の最初に「 ■ 」が入っているので除去
            # また，最後に句点を追加する
            content += (p.text.replace(u'■', '') + u'。').strip()
        else:
            content += p.text.strip()
    return content

def outputList(urls, titles):
    u = open('articles_list.txt', 'w')
    for i in range(len(urls)):
        u.write(titles[i].encode('utf-8'))
        u.write('\n')
        u.write(urls[i])
        if i != len(urls):
            u.write('\n')
    u.close()

def outputContent(content):
    os.mkdir('ARTICLES')
    os.chdir('./ARTICLES')
    for i in range(len(content)):
        # name = i + '.txt'
        c = open(str(i) + '.txt', 'w')
        c.write(content[i].encode('utf-8'))
        c.close()
    os.chdir('../')

def main():
    # フールページのHTMLを取得
    print('PhantomJSを起動')
    full_html = getFullHtml()
    print('PhantomJSを終了')

    # 全ての記事のURLを取得
    print('記事リストを取得開始')
    full_url = getFullURL(full_html)
    print('記事リストを収集完了')

    # 各URLにアクセスし記事タイトルと内容を取得
    titles = []
    content = []
    for url in tqdm(full_url):
        soup = crawler(url)
        titles.append(titleScraiper(soup))
        content.append(contentScraiper(soup))

    outputList(full_url, titles)
    outputContent(content)

if __name__ == '__main__':
    SLEEP_TIME = 1
    main()
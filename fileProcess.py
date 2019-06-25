# -*- coding: utf-8 -*-

import os
import MeCab

# 全てのデータファイルのパスを取得
def getAllFilePaths(directory):
    article_flags = [] # 記事flagのリスト
    for dirpath, dirnames, filenames in os.walk(directory):
        # 不要のものを除く(DS_Storeなど)
        for filename in filenames:
            if filename.endswith('.txt'):
                article_flags.append(filename)
    # 記事パスの整列
    article_flags = sorted(article_flags, key = lambda filename : int(filename.split('.')[0]))
    for article_flag in article_flags:
        yield os.path.join(directory, article_flag)

# 全ての対象ファイルのパスを取得
def getAllAnalysisFilePaths(directory):
    article_flags = []  # 記事flagのリスト
    for dirpath, dirnames, filenames in os.walk(directory):
        # 不要のものを除く(DS_Storeなど)
        for filename in filenames:
            if filename.endswith('.txt'):
                article_flags.append(filename)
    for article_flag in article_flags:
        yield os.path.join(directory, article_flag)

'''
# SlothLibから日本語stopwordを入手(インタネット環境が必要)
def getStopwords():
    slothlib_path = 'http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt'
    slothlib_file = urllib2.urlopen(slothlib_path)
    slothlib_stopwords = [line.decode('utf-8').strip() for line in slothlib_file]
    slothlib_stopwords = [ss.encode('utf-8') for ss in slothlib_stopwords if not ss == '']
    a = open('slothlib_stopwords.txt', 'r')
    for word in slothlib_stopwords:
        a.write(word)
        a.write(',')
    return slothlib_stopwords
'''

# stopwordファイルから日本語stopwordを入手(インタネット環境が不要)
def getStopwords(file_name):
    sw = open(file_name, 'r')
    stop_words = sw.read().split(',')
    sw.close()
    return stop_words

# ファイルから記事の文章を返す
def readContent(path):
    with open(path, 'r') as c:
        return c.read()

# 記事リストを返す
def readArticlesList(file_name):
    al = open(file_name, 'r')
    articles_list = al.readlines()
    al.close()
    return articles_list

# 文章から単語を抽出
def readWords(content, stop_words):
    words = []
    tagger = MeCab.Tagger('-Ochasen -d /usr/local/mecab/lib/mecab/dic/mecab-ipadic-neologd')
    node = tagger.parseToNode(content)
    while node:
        if node.surface in stop_words:
            node = node.next
            continue
        if node.feature.split(',')[0] == '名詞':
            words.append(node.surface)
        '''
        elif node.feature.split(',')[0] == '動詞':
            words.append(node.feature.split(',')[6])
        '''
        node = node.next
    return words

# ファイルから抽出した特徴語を読み取る
def readFeatureWordsFromFile(file_name):
    fw = open(file_name, 'r')
    feature_words = fw.read().split(',')
    fw.close()
    return feature_words

# ファイルから記事ごとに単語文字列を読み取る
def readWordsStringsFromFile(file_name):
    ws = open(file_name, 'r')
    words_strings = ws.read().split(';') # ファイルの中身を読み取り，記事ごとに分割
    ws.close()
    return words_strings

# 単語文字列から単語を読み取る
def readWordsFromWordsStrings(words_strings):
    article_words = [words_string.split(',') for words_string in words_strings] # 分割された単語を記事単語リストに入れる
    return article_words

# ファイルから記事のファイル名を読み取る
def readArticleNames(file_name):
    an = open(file_name, 'r')
    article_names = an.read().split(',')
    an.close()
    return article_names

# ファイルから記事タイトルを読み取る
def readArticleTitles(file_name):
    at = open(file_name, 'r')
    article_titles = at.read().split(',')
    at.close()
    return article_titles

# ファイルから記事タイトルを読み取る
def readArticleURLs(file_name):
    au = open(file_name, 'r')
    article_urls = au.read().split(',')
    au.close()
    return article_urls

# ファイルから記事類似度ベクトルを読み取る
def readArticleSimVecsFromFile(file_name):
    sv = open(file_name, 'r')
    similarityVec_strings = sv.read().split(';')
    sv.close()
    article_similarityVecs = [map(float, similarityVec_string.split(',')) for similarityVec_string in similarityVec_strings]
    return article_similarityVecs

# ファイルから記事の特徴語TF-IDFベクトルを読み取る
def readArticleFeatureTfidfVecsFromFile(file_name):
    aft = open(file_name, 'r')
    feature_tfidfVec_strings = aft.read().split(';')
    aft.close()
    article_feature_tfidfVecs = [map(float, feature_tfidfVec_string.split(',')) for feature_tfidfVec_string in feature_tfidfVec_strings]
    return article_feature_tfidfVecs

# ファイルから記事の隣接ベクトルを読み取る
def readArticleAdjacencyVecsFromFile(file_name):
    aav = open(file_name, 'r')
    adjacencyVec_strings = aav.read().split(';')
    aav.close()
    article_adjacencyVecs = [map(int, adjacencyVec_string.split(',')) for adjacencyVec_string in adjacencyVec_strings]
    return article_adjacencyVecs

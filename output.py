# -*- coding: utf-8 -*-

# 記事類似度ベクトルをファイルに出力
def outputArticlesSimilarityVec(articles, file_name):
    asim = open(file_name, 'w')
    for i, article in enumerate(articles):
        for j, similarity in enumerate(article.similarityVec):
            asim.write(str(similarity))
            if j != len(article.similarityVec) - 1:
                asim.write(',')
        if i != len(articles) - 1:
            asim.write(';')
    asim.close()

# 抽出されたワードをファイルに出力
def outputArticlesWords(articles, file_name):
    aw = open(file_name, 'w')
    for i, article in enumerate(articles):
        for j, word in enumerate(article.words):
            aw.write(word) # 単語を書き込み
            if j != len(article.words) - 1:
                aw.write(',') # 単語リストの末尾でないなら「,」で区切る
        if i != len(articles) - 1:
            aw.write(';') # 末尾なら「;」で区切り，記事の最後を示す
    aw.close()

# 特徴語をファイルに出力
def outputFeatureWords(feature_words, file_name):
    fw = open(file_name, 'w')
    for i, word in enumerate(feature_words):
        fw.write(word)
        if i != len(feature_words) - 1:
            fw.write(',')
    fw.close()

# 記事名をファイルに出力
def outputArticlesName(articles, file_name):
    an = open(file_name, 'w')
    for i, article in enumerate(articles):
        an.write(article.name)
        if i != len(articles) - 1:
            an.write(',')
    an.close()

# 記事タイトルをファイルに出力
def outputArticlesTitle(articles, file_name):
    at = open(file_name, 'w')
    for i, article in enumerate(articles):
        at.write(article.title)
        if i != len(articles) - 1:
            at.write(',')
    at.close()

# 記事URLをファイルに出力
def outputArticlesURL(articles, file_name):
    au = open(file_name, 'w')
    for i, article in enumerate(articles):
        au.write(article.url)
        if i != len(articles) - 1:
            au.write(',')
    au.close()

# 記事の特徴語TF-IDFベクトルをファイルに出力
def outputArticlesFeatureTfidfVec(articles, file_name):
    aft = open(file_name, 'w')
    for i, article in enumerate(articles):
        for j, tfidf in enumerate(article.feature_tfidfVec):
            aft.write(str(tfidf))
            if j != len(article.feature_tfidfVec) - 1:
                aft.write(',')
        if i != len(articles) - 1:
            aft.write(';')
    aft.close()

# 記事の隣接ベクトルをファイルに出力
def outputArticlesAdjacencyVec(articles, file_name):
    aav = open(file_name, 'w')
    for i, article in enumerate(articles):
        for j, e in enumerate(article.adjacencyVec):
            aav.write(str(e))
            if j != len(article.adjacencyVec) - 1:
                aav.write(',')
        if i != len(articles) - 1:
            aav.write(';')
    aav.close()

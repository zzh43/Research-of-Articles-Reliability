# -*- coding: utf-8 -*-

import fileProcess

# 記事モデルの定義
class Article:
    path = []                 # 記事のパス
    name = []                 # 記事のファイル名
    no = []                   # 記事の番号
    title = []                # 記事のタイトル
    url = []                  # 記事のURL
    content = []              # 記事の内容(未処理)
    words = []                # 記事から抽出された前処理済の単語
    keyword = []              # 出現頻度が一番高い特徴語
    all_tfidfVec = []         # 全ての単語のTF-IDFベクトル
    feature_tfidfVec = []     # 特徴語TF-IDFベクトル
    feature_freqVec = []      # 特徴語出現頻度ベクトル
    similarityVec = []        # 記事の特徴語TF-IDF類似度ベクトル
    adjacencyVec = []         # Networkの隣接ベクトル

    def getPath(self, path):
        self.path = path

    def getName(self, name):
        self.name = name

    def getNo(self, no):
        self.no = no

    def getTitle(self, title):
        self.title = title

    def getURL(self, url):
        self.url = url

    def getContent(self):
        self.content = fileProcess.readContent(self.path)

    def getWords(self, words):
        self.words = words

    def contentToWords(self, stop_words):
        self.words = fileProcess.readWords(self.content, stop_words)

    def getAllTfidfVec(self, tfidfVec):
        self.all_tfidfVec = tfidfVec

    def calcFeatureTfidfVec(self, feature_names, feature_words):
        tfidfVec = []
        for feature_word in feature_words:
            tfidfVec.append(self.all_tfidfVec[feature_names.index(feature_word)])
        self.feature_tfidfVec = tfidfVec

    def getFeatureTfidfVec(self, tfidfVec):
        self.feature_tfidfVec = tfidfVec

    def calcFeatureFreqVec(self, feature_words):
        freqVec = []
        for feature_word in feature_words:
            freq = self.words.count(feature_word)
            freqVec.append(freq)
        self.feature_freqVec = freqVec

    def getFeatureFreqVec(self, freqVec):
        self.feature_freqVec = freqVec

    # 特徴語出現頻度が一番の単語をKeywordとする
    def calcKeyword(self, feature_words):
        words = [feature_words[i]
                for i, freq in enumerate(self.feature_freqVec)
                if freq == max(self.feature_freqVec)
                ]

        # 抽出させたKeywordが一つ以上の場合，TF-IDFが高い方とする
        if len(words) != 1:
            tfidfVec = [self.feature_tfidfVec[feature_words.index(word)] for word in words]
            words = [words[i]
                     for i, tfidf in enumerate(tfidfVec)
                     if tfidf == max(tfidfVec)
                     ]
        self.keyword = words[0]

    def calcObjKeyword(self, feature_words):
        word = [feature_words[i]
                for i, freq in enumerate(self.feature_freqVec)
                if freq == max(self.feature_freqVec)
                ]
        self.keyword = word

    def getKeyword(self, word):
        self.keyword = word

    def getSimilarityVec(self, similarityVec):
        self.similarityVec = similarityVec

    def getAdjacencyVec(self, adjacencyVec):
        self.adjacencyVec = adjacencyVec

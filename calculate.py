# -*- coding: utf-8 -*-

from statistics import mean
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# TfidfVectorizerを機能させるためのメソッド
def listReturner(list):
    return list

# 各文書の単語TFIDF値のベクトルを算出
def vecsArray(corpus):
    vectorizer = TfidfVectorizer(
        analyzer = listReturner,
        min_df = 1
    )
    vecs = vectorizer.fit_transform(corpus)
    names = vectorizer.get_feature_names()
    return vecs.toarray(), names
'''
# 特徴語のTF-IDF閾値を再帰的に決める
def getFeatureWords(articles, corpus_tfidf, feature_names, threshold_init, threshold_step):
    # 特徴語リストを宣言
    feature_words = []
    # 初期閾値で特徴語を計算
    for i, feature_name in enumerate(feature_names):
        for tfidf_vec in corpus_tfidf:
            if tfidf_vec[i] >= threshold_init:
                feature_words.append(feature_name)
                break
    
    # 以下のコードで閾値の変化による特徴語の数について解析可能
    # print(len(feature_names))
    # print(len(feature_words))

    # 各記事に特徴語が含まれているかをチェック
    for article in articles:
        # 記事の特徴語頻度ベクトルを計算
        article.calcFeatureFreqVec(feature_words)
        # 含まれていない場合，再帰的に閾値を計算
        if not any(article.feature_freqVec):
            feature_words = getFeatureWords(articles, corpus_tfidf, feature_names, threshold_init - threshold_step, threshold_step)
            print(threshold_init - threshold_step)
            break
    return feature_words
'''

# 特徴語を計算(閾値が決めた場合)
def getFeatureWords(corpus_tfidf, feature_names, threshold):
    feature_words = []
    for i, feature_name in enumerate(feature_names):
        for tfidf_vec in corpus_tfidf:
            if tfidf_vec[i] >= threshold:
                feature_words.append(feature_name)
                break
    return feature_words

# 各文書の特徴語TF-IDF類似度ベクトルを算出し，属性に渡す
def calcSimilarityVec(article):
    vec_pair = [] # 比較するベクトルのリストを宣言
    for i, article_a in enumerate(article):
        similarity_vec = [] # 類似度ベクトルを宣言
        vec_pair.append(article_a.feature_tfidfVec)
        for j, article_b in enumerate(article):
            if i == j:
                similarity_vec.append(1) # 比較記事は同じなら，リストに1を追加
            elif i > j:
                similarity_vec.append(article_b.similarityVec[i]) # 比較したものは同じ数値をリストに追加
            else:
                vec_pair.append(article_b.feature_tfidfVec) # 比較していないものは類似度を算出し，リストに追加
                similarity_vec.append(cosine_similarity(vec_pair, vec_pair)[0][1])
                vec_pair.pop(1) # 比較記事を追い出す
        article_a.getSimilarityVec(similarity_vec) # articleの属性に渡す
        vec_pair.pop(0) # 比較記事を追い出す

'''
# リンク生成の特徴語TF-IDF類似度閾値を算出し，出力する(最小値バージョン)
def calcSimilarityThreshold(articles, keywords):
    threshold = 1
    for keyword in keywords:
        related_articles = []
        for article in articles:
            if article.keyword == keyword:
                related_articles.append(article)
        if len(related_articles) == 1:
            continue
        else:
            for i, related_article_a in enumerate(related_articles):
                for j, related_article_b in enumerate(related_articles):
                    if i < j and related_article_a.similarityVec[articles.index(related_article_b)] < threshold:
                        threshold = related_article_a.similarityVec[articles.index(related_article_b)]
    print(threshold)
'''

# リンク生成の特徴語TF-IDF類似度閾値を算出し，出力する(平均値バージョン)
def calcSimilarityThreshold(articles, keywords):
    keywords_simMean = []
    for keyword in keywords:
        related_articles = []
        for article in articles:
            if article.keyword == keyword:
                related_articles.append(article)
        if len(related_articles) == 1:
            continue
        else:
            keyword_similarity = []
            for i, related_article_a in enumerate(related_articles):
                for j, related_article_b in enumerate(related_articles):
                    if i < j:
                        keyword_similarity.append(related_article_a.similarityVec[articles.index(related_article_b)])
        keywords_simMean.append(mean(keyword_similarity))
    print(mean(keywords_simMean))
    return(mean(keywords_simMean))

# 特徴語TF-IDF類似度を閾値で隣接ベクトルに変更
def simToAdjVec(articles, simThreshold):
    for article in articles:
        adjacencyVec = []
        for similarity in article.similarityVec:
            if similarity >= simThreshold:
                adjacencyVec.append(1)
            else:
                adjacencyVec.append(0)
        article.getAdjacencyVec(adjacencyVec)

# 推定対象の特徴語TF-IDFベクトルを算出し，属性に渡す
def calcObjFeatureTfidfVec(article_obj, article_data, feature_words):
    obj_feature_tfidf_vec = [] # 特徴語TF-IDF類似度ベクトルを宣言
    words_corpus = [] # 全記事wordコーパスを宣言
    for article in article_data:
        words_corpus.append(article.words)
    words_corpus.append(article_obj.words) # words_corpusの最後に対象記事の単語を追加
    corpus_tfidf, feature_names = vecsArray(words_corpus) # コーパス全体のTF-IDF行列と対応する単語を取得
    for feature_word in feature_words:
        if feature_word in feature_names:
            obj_feature_tfidf_vec.append(corpus_tfidf[len(article_data)][feature_names.index(feature_word)])
        else:
            obj_feature_tfidf_vec.append(0)
    article_obj.getFeatureTfidfVec(obj_feature_tfidf_vec)

# 推定対象の特徴語TF-IDF類似度ベクトルを算出し，属性に渡す
def calcObjFeatureSimVec(article_obj, article_data):
    obj_feature_simVec = [] # 類似度ベクトルを宣言
    vec_pair = [] # cos類似度を計算したい特徴語TF-IDFベクトルのペア
    vec_pair.append(article_obj.feature_tfidfVec) # 推定対象の特徴語TF-IDFベクトルを追加
    for article in article_data: # データベースにある各記事において
        vec_pair.append(article.feature_tfidfVec) # 記事特徴語TF-IDFベクトルをリストに追加
        similarity = cosine_similarity(vec_pair, vec_pair)[0][1] # cos類似度を計算
        obj_feature_simVec.append(similarity) # 類似度を類似度ベクトルに追加
        # article.feature_tfidfVec.append(similarity) # check用
        vec_pair.pop(1) # 比較記事を追い出す
    obj_feature_simVec.append(1) # 推定対象記事ベクトルの最後に1を追加
    article_obj.getSimilarityVec(obj_feature_simVec) # 推定対象記事の属性に渡す

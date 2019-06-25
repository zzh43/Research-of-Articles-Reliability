# -*- coding: utf-8 -*-

import fileProcess
import articleModel
import calculate
import network
import pandas as pd

STOP_WORDS_FILE_NAME = 'slothlib_stopwords.txt'
FEATURE_WORDS_FILE_NAME = 'feature_words.txt'
ARTICLES_WORDS_FILE_NAME = 'articles_words.txt'
ARTICLES_NAME_FILE_NAME = 'articles_name.txt'
ARTICLES_TITLE_FILE_NAME = 'articles_title.txt'
ARTICLES_URL_FILE_NAME = 'articles_url.txt'
ARTICLES_SIMILARITYVEC_FILE_NAME = 'articles_similarityVec.txt'
ARITCLES_FEATURE_TFIDFVEC_FILE_NAME = 'article_feature_tfidfVec.txt'
ARTICLES_ADJACENCYVEC_FILE_NAME = 'articles_adjacencyVec.txt'
OBJ_ARTICLES_DIR = './OBJECT'
IMAGE_DIR = './IMAGE/'
RELIABLE_NETWORK_FEATURE_CSV_FILE_NAME = 'reliable_network_feature.csv'
UNRELIABLE_NETWORK_FEATURE_CSV_FILE_NAME = 'unreliable_network_feature.csv'

THRESHOLD = 類似度閾値
STEP = ステップ数

if __name__ == '__main__':
    #####################################
    # 以下は記事データベースファイルからの読取#
    #####################################
    print('対象データベースからデータを読み取り開始')
    # 各属性ファイルから，articleの各属性を読み取り，属性リストを生成
    article_names = fileProcess.readArticleNames(ARTICLES_NAME_FILE_NAME)
    article_titles = fileProcess.readArticleTitles(ARTICLES_TITLE_FILE_NAME)
    article_urls = fileProcess.readArticleURLs(ARTICLES_URL_FILE_NAME)
    words_strings = fileProcess.readWordsStringsFromFile(ARTICLES_WORDS_FILE_NAME)
    article_words = fileProcess.readWordsFromWordsStrings(words_strings)
    article_similarityVecs = fileProcess.readArticleSimVecsFromFile(ARTICLES_SIMILARITYVEC_FILE_NAME)
    article_feature_tfidfVecs = fileProcess.readArticleFeatureTfidfVecsFromFile(ARITCLES_FEATURE_TFIDFVEC_FILE_NAME)
    article_adjacencyVecs = fileProcess.readArticleAdjacencyVecsFromFile(ARTICLES_ADJACENCYVEC_FILE_NAME)
    print('対象データベースからデータを読み取り終了')

    #######################################
    # 以下は記事データベースのインスタンスの生成#
    #######################################
    print('記事データベースのインスタンスを生成開始')
    # articleリストを宣言
    article_data = []
    # articleインスタンスを生成
    for i, article_name in enumerate(article_names):
        article_instance = articleModel.Article()
        article_instance.getName(article_names[i])
        article_instance.getTitle(article_titles[i])
        article_instance.getURL(article_urls[i])
        article_instance.getNo(i)
        article_instance.getWords(article_words[i])
        article_instance.getSimilarityVec(article_similarityVecs[i])
        article_instance.getFeatureTfidfVec(article_feature_tfidfVecs[i])
        article_instance.getAdjacencyVec(article_adjacencyVecs[i])
        article_data.append(article_instance) # インスタンスをarticleリストに追加
    print('記事データベースのインスタンスを生成終了')

    #########################
    # 以下は対象記事の類似度推定#
    #########################
    print('対象記事を解析開始')
    # ストップワードを取得
    stop_words = fileProcess.getStopwords(STOP_WORDS_FILE_NAME)

    # 特徴語を取得
    feature_words = fileProcess.readFeatureWordsFromFile(FEATURE_WORDS_FILE_NAME)

    # 全ての対象記事のパスを取得
    obj_file_paths = list(fileProcess.getAllAnalysisFilePaths(OBJ_ARTICLES_DIR))

    obj_article = []
    for i, path in enumerate(obj_file_paths):
        obj_instance = articleModel.Article() # articleインスタンスを生成
        obj_instance.getPath(path)
        obj_instance.getName(path.split('/')[2])
        obj_instance.getNo(len(article_data))
        obj_instance.getContent()  # ファイルを読み取る
        obj_instance.contentToWords(stop_words)  # articleの内容からワードを抽出
        calculate.calcObjFeatureTfidfVec(obj_instance, article_data, feature_words) # 推定対象の特徴語TF-IDFベクトルを算出
        calculate.calcObjFeatureSimVec(obj_instance, article_data) # 推定対象の特徴語TF-IDF類似度を算出
        calculate.simToAdjVec(list([obj_instance]), THRESHOLD) # 推定対象の隣接ベクトルを算出
        print('対象' + obj_instance.name + ':')
        for i, a in enumerate(obj_instance.similarityVec):
            if a >= THRESHOLD:
                print('記事' + str(i) + ':' + str(a))
        obj_article.append(obj_instance) # 対象記事リストに追加
        del obj_instance # instanceを削除
    print('対象記事を解析終了')

    ######################################################
    # 以下は関連記事ネットワークの可視化と特徴量のCSVファイル出力#
    ######################################################
    print('解析結果を出力開始')
    df = pd.DataFrame(columns = ['NAME', 'DEGREE', 'CLOSENESS', 'BETWEENNESS', 'DENSITY', 'CLUSTER'])
    for obj in obj_article:
        df = df.append(network.constructNetwork(obj, article_data, STEP, IMAGE_DIR), ignore_index = True)
    df.to_csv(RELIABLE_NETWORK_FEATURE_CSV_FILE_NAME, index = False, encoding = 'utf-8')
    # df.to_csv(UNRELIABLE_NETWORK_FEATURE_CSV_FILE_NAME, index = False, encoding = 'utf-8')
    print('解析結果を出力終了')

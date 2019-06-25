# -*- coding: utf-8 -*-

import fileProcess
import articleModel
import calculate
import output
from tqdm import tqdm

#入力ファイルのディレクトリ
DATABESE_ARTICLES_DIR = './ARTICLES'
ARTICLES_LIST_NAME = 'articles_list.txt'
STOP_WORDS_FILE_NAME = 'slothlib_stopwords.txt'

#出力ファイルのディレクトリ
FEATURE_WORDS_FILE_NAME = 'feature_words.txt'
ARTICLES_SIMILARITYVEC_FILE_NAME = 'articles_similarityVec.txt'
ARTICLES_WORDS_FILE_NAME = 'articles_words.txt'
ARTICLES_NAME_FILE_NAME = 'articles_name.txt'
ARTICLES_TITLE_FILE_NAME = 'articles_title.txt'
ARTICLES_URL_FILE_NAME = 'articles_url.txt'
ARITCLES_FEATURE_TFIDFVEC_FILE_NAME = 'article_feature_tfidfVec.txt'
ARTICLES_FEATURE_FREQVEC_FILE_NAME = 'articles_feature_freqVec.txt'
ARTICLES_KEYWORD_FILE_NAME = 'articles_keyword.txt'
ARTICLES_ADJACENCYVEC_FILE_NAME = 'articles_adjacencyVec.txt'

#特徴語TF-IDF閾値を決めるグローバル変数
TFIDF_THRESHOLD_INIT = 閾値の初期値
TFIDF_THRESHOLD_STEP = 閾値の刻み
# システムを利用して計算した値を入力
THRESHOLD = 特徴語TF-IDF閾値

if __name__ == '__main__':
    # 全ての記事のパスを取得
    file_paths = list(fileProcess.getAllFilePaths(DATABESE_ARTICLES_DIR))

    # ストップワードを取得
    stop_words = fileProcess.getStopwords(STOP_WORDS_FILE_NAME)

    # 記事リストを取得
    articles_list = fileProcess.readArticlesList(ARTICLES_LIST_NAME)

    articles = [] # articleのクラスリストを宣言
    words_corpus = [] # 全記事のwordコーパス
    # 記事クラスリストの生成
    print('記事リストを生成開始')
    for i, file_path in enumerate(tqdm(file_paths)):
        article_instance = articleModel.Article() # articleインスタンスを生成
        article_instance.getPath(file_path)  # articleのパスを与える
        article_instance.getName(file_path.split('/')[2]) #articleのファイル名を与える
        article_instance.getNo(i)  # articleの番号を与える
        article_instance.getTitle(articles_list[i * 2].replace('\n', '')) # articleのタイトルを与える
        article_instance.getURL(articles_list[i * 2 + 1].replace('\n', '')) # articleのURLを与える
        article_instance.getContent() # ファイルを読み取る
        article_instance.contentToWords(stop_words) # articleの内容からワードを抽出
        words_corpus.append(article_instance.words) # articleの単語をコーパスのリストに追加
        articles.append(article_instance) # インスタンスをarticleリストに追加
    print('記事リストが生成終了')

    # 全記事のTF-IDF値と対応する単語を取得
    print('全記事のTF-IDF値を計算開始')
    corpus_tfidf, feature_names = calculate.vecsArray(words_corpus) #コーパス全体のTF-IDF行列と対応する単語を取得
    print('全記事のTF-IDF値が計算終了')

    '''
    # 特徴語抽出(閾値が未定の場合)
    print('特徴語を抽出開始')
    feature_words = calculate.getFeatureWords(articles, corpus_tfidf, feature_names, TFIDF_THRESHOLD_INIT, TFIDF_THRESHOLD_STEP)
    print('特徴語が抽出終了')
    '''

    # 特徴語抽出(閾値が決めた場合)
    print('特徴語を抽出開始')
    feature_words = calculate.getFeatureWords(corpus_tfidf, feature_names, THRESHOLD)
    print('特徴語が抽出終了')

    # 特徴語TF-IDFベクトルと出現頻度ベクトルを計算
    print('記事を解析開始')
    keywords = [] # 全記事のキーワードリストを宣言
    for i, article in enumerate(tqdm(articles)):
        article.getAllTfidfVec(corpus_tfidf[i]) # artitleの全ての単語のTF-IDFベクトルを与える
        article.calcFeatureTfidfVec(feature_names, feature_words) # articleの特徴語TF-IDFベクトルを計算
        article.calcFeatureFreqVec(feature_words) # articleの特徴語の出現頻度ベクトルを計算
        article.calcKeyword(feature_words) # articleのkeywordを抽出
        keywords.append(article.keyword) # articleのkeywordをリストに追加
        print(article.keyword)

    print('各記事の類似度ベクトルを算出中')
    calculate.calcSimilarityVec(articles) # 各記事の特徴語TF-IDF類似度ベクトルを算出

    print('リンク生成の特徴語TF-IDF類似度閾値を算出中')
    simThreshold = calculate.calcSimilarityThreshold(articles, keywords) # リンク生成の特徴語TF-IDF類似度閾値を算出

    print('ネットワークを生成中')
    calculate.simToAdjVec(articles, simThreshold)

    print('記事が解析終了')

    output.outputArticlesWords(articles, ARTICLES_WORDS_FILE_NAME) # 抽出されたワードをファイルに出力(必須)
    output.outputFeatureWords(feature_words, FEATURE_WORDS_FILE_NAME) # 特徴語をファイルに出力(必須ではない)
    output.outputArticlesName(articles, ARTICLES_NAME_FILE_NAME) # ファイル名をファイルに出力(必須ではない)
    output.outputArticlesTitle(articles, ARTICLES_TITLE_FILE_NAME) # 記事タイトルをファイルに出力(必須ではない)
    output.outputArticlesURL(articles, ARTICLES_URL_FILE_NAME) # 記事URLをファイルに出力(必須ではない)
    output.outputArticlesSimilarityVec(articles, ARTICLES_SIMILARITYVEC_FILE_NAME) # 記事類似度ベクトルをファイルに出力(必須)
    output.outputArticlesFeatureTfidfVec(articles, ARITCLES_FEATURE_TFIDFVEC_FILE_NAME) # 記事の特徴語TF-IDFベクトルをファイルに出力(必須)
    output.outputArticlesAdjacencyVec(articles, ARTICLES_ADJACENCYVEC_FILE_NAME) # 記事の隣接ベクトルをファイルに出力

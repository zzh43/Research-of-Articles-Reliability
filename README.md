# Research-of-Articles-Reliability
This repository is the source code of my research that I used Relative Articles Network to analyze articles' reliability.
***

## CRAWLER
### SOURCE CODE
- nikkei_style.py: crawler of [Nikkei_Style](https://style.nikkei.com)  
- MEDLEY.py: crawler of [MEDLEY](https://medley.life/news/)  
- DOCTORSME.py: crawler of [Doctorsme](https://doctors-me.com/)

### 実行環境
- OS: macOS High Sierra 10.13.3  
- Python: 2.7.14  
- beautifulSoup4: 4.6.0  
- requests: 2.18.4  
- selenium: 3.7.0  
- tqdm: 4.19.4  

### 実行方法
そのまま実行すれば良い．  
スクリプトファイルと同じディレクトリに，  
新しくARTICLESファイルが生成され，記事が中に保存している．  
記事のタイトルとURLは記事リストファイルに保存している．
***

## ANALYZE SYSTEM
### SOURCE CODE
- preprocess.py  : 前処理を行うスクリプト  
- analysis.py    : 対象記事を評価するスクリプト  
- articleModel.py: 記事データの保持および記事に関する各種データの計算のに関するスクリプト(複雑な計算はcalculate.pyで実装)  
- calculate.py   : 複雑な計算を実装するスクリプト  
- fileProcess.py : ファイルからの読取のスクリプト  
- output.py      : 計算結果および中間ファイルの出力のスクリプト  
- network.py     : 関連記事ネットワークの生成，可視化およびネットワーク特徴量の抽出のスクリプト  

### 実行環境
- VirtualBox: バージョン5.2.2 r119230 (Qt5.6.2)  
- ubuntu: 16.04 LTS  
- PyCharm: 2017.3.3 (Professional Edition)  
- python: 2.7  
- pandas: 0.22.0  
- statistics: 1.0.3.5  
- scikit-learn: 0.19.1  
- numpy: 1.13.3  
- mecab-python: 0.996  
- Mecab辞書: Neologd(2018/1/10更新)  
- networkx: 2.0  
- matplotlib: 1.5.1  
- tqdm: 4.19.5  

### 実験で得た閾値
- 特徴語TF-IDF値閾値: 0.42  
- 類似度閾値: 0.51  

### 実行方法
1. 「各ファイルの説明」にあるファイルを同じディレクトリに置く  
2. 「システムの入力ファイル」にあるファイルを同じディレクトリに置く  
3. preprocess.pyの64行目のコメント記号を消し，106行目にコメント記号をつける  
4. calculate.pyの21行目から45行目までのコメント記号を消し，48行目から56行目までをコメントアウトする  
5. 論文本文の9ページのアルゴリズムに従い，グローバル変数である閾値の初期値と刻みの値を入れて，閾値を決めるまでpreprocess.pyを実行する  
6. 計算した閾値をpreprocess.pyのグローバル変数THRESHOLDに入力する  
7. 106行目のコメント記号を消し，64行目にコメント記号をつける  
8. calculate.pyの48行目から56行目までのコメント記号を消し，21行目から45行目までをコメントアウトして，preprocess.pyを実行する  
9. 実行し終わった後，データベースとなる記事に対して前処理を行って，生成した各種ファイルは同じディレクトリに生成され，関連記事ネットワークを構築するための類似度閾値も出力される  
10. analysis.pyファイルに類似度閾値を入れ，ステップ数を指定する  
11. 信頼性がある・ない記事を解析する場合に対し，analysis.pyの103・104行をコメントしたりコメントアウトしたりする  
12. analysis.pyを実行する  
13. 構築した関連ネットワークの図面は新規されたIMAGEファイルに出力する  
14. 信頼できる・できない記事の関連記事ネットワークの特徴量は(un)reliable.csvに出力する  
15. 出力したファイルに対し，Analysisファイル内のスクリプトを用いて解析する  

### 入力ファイル
- ARTICLES: 記事本文を保存するファイル  
- articles_list.txt: 記事リストのファイル  
- slothlib_stopword.txt: ストップワードを保存するファイル  ([ここ](http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt)からダウンロードしたもの)  
- OBJECT: 対象記事を保存するファイル  

### システムの出力ファイル
**preprocess.pyの出力ファイル**  
- feature_words.txt: 各記事から抽出した特徴語を保存するファイル  
- articles_similarityVec.txt: 各記事記事類似度行列を保存するファイル  
- articles_words.txt: 各記事から抽出したワードを保存するファイル  
- articles_name.txt: 各記事のファイルのファイル名を保存するファイル  
- articles_title.txt: 各記事のタイトルを保存するファイル  
- articles_url.txt: 各記事のURLを保存するファイル  
- article_feature_tfidfVec.txt: 各記事の特徴語に対するTF-IDF値を保存するファイル  
- articles_adjacencyVec.txt: 記事データベースの関連記事ネットワークの隣接行列を保存するファイル  
**analysis.pyの出力ファイル**  
- reliable_network_feature.csv: 信頼できる記事の関連記事ネットワークの特徴量を保存するファイル  
- unreliable_network_feature.csv: 信頼できない記事の関連記事ネットワークの特徴量を保存するファイル  
- IMAGE: 構築した関連記事ネットワークの図を保存するファイル  

***
## DATA ANALYZE FILES
### SOURCE CODE
- docNoChanger.py: 収集した三つのサイトの記事を1つのデータベースに統合するためのスクリプトである．記事の番号を振り替わる機能を持つ．記事元と出力する場所と開始番号をスクリプトに書き変えるする必要がある  
- eva_logisitc.py: 関連記事ネットワークの特徴量CSVファイルを読み取り，ロジスティック回帰で学習し，さらに10分割交差検証を行うスクリプトである．スクリプトにシステムで出力された信頼できる・できない記事の関連記事ネットワークの特徴量のCSVファイルの場所を記入する必要がある  
- eva_randomForest.py: 関連記事ネットワークの特徴量CSVファイルを読み取り，ランダムフォレストで学習し，さらに10分割交差検証を行うスクリプトである．スクリプトにシステムで出力された信頼できる・できない記事の関連記事ネットワークの特徴量のCSVファイルの場所を記入する必要がある  
- outputHisgram.py: 指定されたCSVファイルに対し，ヒストグラムを出力するスクリプトである．スクリプトにシステムで出力された信頼できる・できない記事の関連記事ネットワークの特徴量のCSVファイルの場所を記入する必要がある  
pdf2txt.py: PDFファイルから文字を読み取り，ファイルに出力するスクリプトである．本実験では使わなかった  

### 実行環境
- OS: macOS High Sierra 10.13.3  
- Python: 2.7.14  
- pandas: 0.20.3  
- matplotlib: 2.1.0  
- scikt-learn: 0.19.0  
- statistics: 1.0.3.5  
- numpy: 1.13.3 
- tqdm: 4.19.4  

### 実行方法
スクリプトにCSVファイルの場所を書き換えたら，そのままで実行すれば良い．

# -*- coding: utf-8 -*-

import os.path
from tqdm import tqdm

INPUT_DIR = '記事元の場所'
OUTPUT_DIR = '出力する場所'
START_NO = 記事の開始番号

# 全ての記事のパスを取得
def getAllDocPaths(path):
    doc_flags = [] # 記事flagのリスト
    for dirpath, dirnames, filenames in os.walk(path):
        # 不要のものを除く(DS_Storeなど)
        for filename in filenames:
            if filename.endswith('.txt'):
                doc_flags.append(filename)
    # 記事パスの整列
    doc_flags = sorted(doc_flags, key = lambda filename : int(filename.split('.')[0]))
    for doc_flag in doc_flags:
        yield os.path.join(path, doc_flag)

# 記事の内容を取得
def readContent(path):
    with open(path, 'r') as c:
        return c.read()

# 記事を出力
def outputDoc(content, file_name):
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    d = open(OUTPUT_DIR + '/' + file_name, 'w')
    d.write(content)
    d.close()

def main():
    # 全ての記事のパスを取得
    doc_paths = list(getAllDocPaths(INPUT_DIR))
    print('処理開始')
    for i, doc_path in enumerate(tqdm(doc_paths)):
        # 記事の内容を取得
        doc_content = readContent(doc_path)
        # 記事を出力
        outputDoc(doc_content, str(START_NO + i) + '.txt')
    print('処理終了')

if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
from sklearn import metrics
from sklearn.metrics import classification_report
from statistics import mean
import pandas as pd
import numpy as np

RELIABLE_PATH = '信頼できる記事のCSVファイルの場所'
UNRELIABLE_PATH = '信頼できない記事のSVファイルの場所'
KFOLD = 10

def readDataFromCsv(path):
    '''
    data = pd.read_csv(path).values.tolist()
    for vec in data:
         vec.pop(0)
    return data
    '''
    data = pd.read_csv(path).drop('NAME', axis = 1)
    return data

def evaluation(X, y):
    train_mean = []
    test_mean = []
    kf = KFold(n_splits = KFOLD)
    lr = LogisticRegression()
    for train_index, test_index in kf.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        lr.fit(X_train, y_train)
        train_mean.append(lr.score(X_train, y_train))
        print(lr.score(X_train, y_train))
        y_predict = lr.predict(X_test)
        test_mean.append(lr.score(X_test, y_test))
        print(metrics.accuracy_score(y_test, y_predict))
        print classification_report(y_test, y_predict)
        print('\n')
    print('訓練データの平均精度: ' + str(mean(train_mean)))
    print('テストデータの平均精度: ' + str(mean(test_mean)))
def main():
    reliableData = readDataFromCsv(RELIABLE_PATH)
    unreliableData = readDataFromCsv(UNRELIABLE_PATH)
    X = np.vstack((reliableData, unreliableData))

    reliableTarget = np.ones(len(reliableData))
    unreliableTarget = np.zeros(len(unreliableData))
    y = np.append(reliableTarget, unreliableTarget)

    evaluation(X, y)


if __name__ == '__main__':
    main()

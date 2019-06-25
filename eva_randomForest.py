# -*- coding: utf-8 -*-

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold
from sklearn import metrics
from sklearn.metrics import f1_score
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
    train_sum = []
    test_sum = []
    kf = KFold(n_splits = KFOLD)
    forest = RandomForestClassifier(n_estimators = 30, random_state = 10)
    for train_index, test_index in kf.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        forest.fit(X_train, y_train)
        train_sum.append(forest.score(X_train, y_train))
        print(forest.score(X_train, y_train))
        test_sum.append(forest.score(X_test, y_test))
        print(forest.score(X_test, y_test))
        feature = forest.feature_importances_
        print feature
        print('\n')
    print('訓練データの平均精度: ' + str(mean(train_sum)))
    print('テストデータの平均精度: ' + str(mean(test_sum)))

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

# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt

RELIABLE_PATH = '信頼できる記事のCSVファイルの場所'
UNRELIABLE_PATH = '信頼できない記事のSVファイルの場所'
COLUMN = ['DEGREE', 'CLOSENESS', 'BETWEENNESS', 'DENSITY', 'CLUSTER']

def readDataFromCsv(path):
    data = pd.read_csv(path)
    return data

def outputHistgram(column, data_r, data_u):
    labels = ['RELIABLE', 'UNRELIABLE']
    plt.hist([data_r[column], data_u[column]], label = labels)
    plt.title(column)
    plt.legend(fontsize = 15)
    plt.show()

def main():
    reliableData = readDataFromCsv(RELIABLE_PATH)
    unreliableData = readDataFromCsv(UNRELIABLE_PATH)

    for column in COLUMN:
        outputHistgram(column, reliableData, unreliableData)

if __name__ == '__main__':
    main()

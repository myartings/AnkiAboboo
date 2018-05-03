#!/usr/bin/python
#-*-coding:utf-8-*-
"""
My first python program
"""
import re
import os
#import sys
import csv
#from sys import argv
import glob
import time
import pickle
import shutil

output = "Tobeimport.csv"
mediaPath = r"C:\Users\myartings\AppData\Roaming\Anki2\用户1\collection.media"
importWordsPath = mediaPath + '\\' + 'importWords'

def Main():
    itemlist = []
    with open(importWordsPath, 'rb') as fp:
        itemlist = pickle.load(fp)
    print(itemlist)

    curpath = os.getcwd()
    folderList = []
    for x in os.listdir(curpath):
        if os.path.isdir(x):
            folderList.append(x)
    folderList.sort()
    print(folderList)
    lrcfiles = curpath + "\\" + folderList[-1] + "//*.lrc"
    print(lrcfiles)
    flist = glob.glob(lrcfiles)
    fo = open(output, 'w+', encoding='utf-8')
    writer = csv.writer(fo)
    pattern1 = re.compile(r'00]([\s\S]*) \t')
    pattern2 = re.compile(r'\t([\s\S]*)')

    wordFile = curpath + "//word.txt"
    wordList = []
    with open(wordFile, 'r') as f:
        for line in f:
            line = line.strip('\n')
            wordList.append(line)

    i = 0
    for f in flist:
        i = i + 1
        print("i: ", i)
        fh = open(f, 'r')
        content = fh.read()
        english = pattern1.findall(content)
        chinese = pattern2.findall(content)

        if content not in itemlist:
            itemlist.append(content)
        else:
            continue

        print(content)
        print(english)
        print(chinese)

        mp3file = f[:-3] + "mp3"
        newname = mediaPath + "\\" + str(time.time()) + str(i) + ".mp3"
        print(mp3file)
        print(newname)

        os.rename(mp3file, newname)
        print("rename")

        audio = "[sound:" + newname + "]"
        stem = ""
        for word in wordList:
            if word in content:
                stem = word
                wordList.remove(word)
                break

        if not english:
            answer = content[10:]
        else:
            answer = english[0] + "   " + audio
        writer.writerow([stem, audio, answer])
        fh.close()

    print(itemlist)
    with open(importWordsPath, 'wb') as fp:
        pickle.dump(itemlist, fp)

    del writer
    fo.close()
    # shutil.rmtree(curpath + "\\" + folderList[-1])
if __name__ == "__main__":
    Main()
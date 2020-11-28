# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 01:34:54 2020

@author: mehdi
"""
import csv
import datetime

archiveFile = "visitedUrls.csv"
def archieveUrl(url):
    with open(archiveFile,"a",newline='') as f:
        write = csv.writer(f,delimiter=",")
        write.writerow([str(url),datetime.datetime.now()])

def loadVisitedUrls():
    rows =[]
    try:
        with open(archiveFile,"r",newline='') as f:
            reader = csv.reader(f,delimiter=",")
            [rows.append(item[0]) for item in reader]
            '''
            for item in reader:
                rows.append(item)
            '''
    except Exception as ex:
        print("no recent history !")
    return rows

''' 
# test archieveUrl()

ll =["hmida","abbas","sagna"]
for item in ll:
    archieveUrl(item)

'''
'''
#test loadVisitedUrls

ll =loadVisitedUrls()
for item in ll:
    print(item)
'''
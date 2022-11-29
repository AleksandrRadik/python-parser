import requests
import tokenize_uk
from docx import Document
from bs4 import BeautifulSoup
import csv
import os
import re

def getPageText(url, arg, type):
  resp = requests.get(url).text
  if (type == 0):
    soup = BeautifulSoup(resp, 'html.parser').find(id=arg)
  elif (type == 1):
    soup = BeautifulSoup(resp, 'html.parser').find(class_=arg)
  return soup.get_text()

def getDocxText(filename):
  wordDoc = Document(filename)
  fullText = []
  for para in wordDoc.paragraphs:
    fullText.append(para.text)
  return '\n'.join(fullText)

def parseText(text):
  if text == "":
      return []
  text = text.replace("\n", " ")
  tokenizedSnt = tokenize_uk.tokenize_sents(text)
  result = []
  for snt in tokenizedSnt:
    if len(snt) > 10:
      result.append(snt)
  return result

def writeToCsv(sentencesArr, lng, filename, dataType):
  if lng == 0:
    encdoing = 'cp1251'
  elif lng == 1:
    encdoing = 'utf-8'
  filename = filename + '.csv' if(filename) else 'results.csv'
  with open(filename, "a", newline="", encoding=encdoing) as csvfile:
    columns = ['text','target']
    writer = csv.DictWriter(csvfile, fieldnames=columns)
    
    if os.path.isfile(filename) == False:
      writer.writeheader()

    for str in sentencesArr:
      row = [str, dataType]
      writer = csv.writer(csvfile)
      writer.writerow(row)

def logger(logText):
  with open("logs.txt", "a", encoding='utf-8') as logFile:
    logFile.write(logText + '\n')


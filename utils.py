import requests
import tokenize_uk
import nltk.data
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

def parseText(text, lng):
  if text == "":
      return []
  text = text.replace("\n", " ")
  text = text.replace("׳", "")
  text = text.replace("°", "")
  text = text.replace("˚", "")
  result = []
  if lng == 0:
    tokenizedSnt = tokenize_uk.tokenize_sents(text)
    for snt in tokenizedSnt:
      if len(snt) > 10:
        result.append(snt)
  elif lng == 1:
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    tokenizedSnt = tokenizer.tokenize(text)
    for snt in tokenizedSnt:
      if len(snt) > 10:
        result.append(snt)
  return result

def writeToCsv(sentencesArr, lng, filename, dataType):
  if lng == 0:
    encdoing = 'cp1251'
  elif lng == 1:
    encdoing = 'utf-8'
  with open(filename, "a", newline="", encoding=encdoing) as csvfile:
    columns = ['text','target']
    writer = csv.writer(csvfile, delimiter=",")
    writer.writerow(columns)  # write header
    writer.writerows(convertTextToCsvRows(sentencesArr, dataType)) # write data

def convertTextToCsvRows(text, dataType):
  csvRows = []
  for str in text:
      csvRows.append([str, dataType])
  return csvRows

def logger(logText):
  with open("logs.txt", "a", encoding='utf-8') as logFile:
    logFile.write(logText + '\n')

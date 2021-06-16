import requests
from docx import Document
from bs4 import BeautifulSoup
import csv
import os

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
  text = text.replace(",", "")
  idx1 = 0
  idx2 = 0
  sntArr = []
  while True:
    point = text.find(".", idx1+1)
    if point == -1:
        break
    if point == (len(text)-1):
        if idx2 == 0:
            ind1 = int((int(idx2)))
        else:
            ind1 = int((int(idx2) + 2))
        ind2 = int((int(point) + 1))
        sntArr.append(text[ind1:ind2])
        idx2 = point
    elif((text[point+2].isupper()) and (text[point-2] != " ") and (text[point-2] != ".") and (text[point-3] != " ") and (text[point-1].isdigit() == False) and (text[point-2].isdigit() == False) ):
        if idx2 == 0:
            ind1 = int((int(idx2)))
        else:
            ind1 = int((int(idx2) + 2))
        ind2 = int((int(point)+1))
        sntArr.append(text[ind1:ind2])
        idx2 = point

    idx1 = point
  return sntArr

def writeToCsv(sentencesArr, lng, filename):
  if lng == 0:
    encdoing = 'cp1251'
  elif lng == 1:
    encdoing = 'utf-8'
  filename = filename + '.csv'
  with open(filename, "a", newline="", encoding=encdoing) as csvfile:
    columns = ['text','target']
    writer = csv.DictWriter(csvfile, fieldnames=columns)
    
    if os.path.isfile(filename) == False:
      writer.writeheader()

    for str in sentencesArr:
      row = [str, "0"]
      writer = csv.writer(csvfile)
      writer.writerow(row)


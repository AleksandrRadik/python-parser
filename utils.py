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
  # text = text.replace(",", "")
  # idx1 = 0
  # idx2 = 0
  # sntArr = []
  # while True:
  #   point = text.find(".", idx1+1)
  #   if point == -1:
  #       break
  #   if point == (len(text)-1):
  #       if idx2 == 0:
  #           ind1 = int((int(idx2)))
  #       else:
  #           ind1 = int((int(idx2) + 2))
  #       ind2 = int((int(point) + 1))
  #       sntArr.append(text[ind1:ind2])
  #       idx2 = point
  #   elif((text[point+2].isupper()) and (text[point-2] != " ") and (text[point-2] != ".") and (text[point-3] != " ") and (text[point-1].isdigit() == False) and (text[point-2].isdigit() == False) ):
  #       if idx2 == 0:
  #           ind1 = int((int(idx2)))
  #       else:
  #           ind1 = int((int(idx2) + 2))
  #       ind2 = int((int(point)+1))
  #       sntArr.append(text[ind1:ind2])
  #       idx2 = point

  #   idx1 = point
  # return sntArr
  result = tokenize_uk.tokenize_sents(text)
  # logger('Parse text')
  # for snt in result:
  #   logger(snt)
  logger(str(len(result)))
  return result

def writeToCsv(sentencesArr, lng, filename, dataType):
  logger('sentencesArr')
  logger(sentencesArr[0])
  try:
    logger(str(len(sentencesArr)))
  except:
    print("Something went wrong")
  
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
    

# def clean_text(text):
#   # Remove Emojis
#   emoji_pattern = re.compile("["
#   u"\U0001F600-\U0001F64F"  # emoticons
#   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
#   u"\U0001F680-\U0001F6FF"  # transport & map symbols
#   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
#   u"\U00002702-\U000027B0"
#   u"\U000024C2-\U0001F251"
#   "]+", flags=re.UNICODE)
#   text = emoji_pattern.sub(r'', text)
#   ## Convert words to lower case and split them
#   text = text.lower().split()
#   # Clean the text
#   text = re.sub(r"[^A-Za-z0-9^,!.\/'+-=]", " ", text)
#   text = re.sub(r",", " ", text)
#   text = re.sub(r"!", " ! ", text)
#   text = re.sub(r"\/", " ", text)
#   text = re.sub(r"\^", " ^ ", text)
#   text = re.sub(r"\+", " + ", text)
#   text = re.sub(r"\-", " - ", text)
#   text = re.sub(r"\=", " = ", text)
#   text = re.sub(r"'", " ", text)
#   text = re.sub(r"(\d+)(k)", r"\g<1>000", text)
#   text = re.sub(r":", " : ", text)
#   text = re.sub(r"\0s", "0", text)
#   text = text.split()
#   return text

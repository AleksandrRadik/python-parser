import utils
import nltk.data
import PySimpleGUI as sg

sg.theme("DarkBlue")
nltk.download('popular')
## Layout for ui
layout = [
    [
      sg.Frame(layout=[[sg.Radio('Укр', 'rad1', key='ua', default=True),  sg.Radio('Англ', 'rad1')]],
      title='Оберіть мову'),
      sg.Frame(layout=[[sg.Radio('Web', 'rad2', key='web', enable_events=True),  sg.Radio('Docx', 'rad2', key='docx', default=True, enable_events=True)]],
      title='Оберіть тип парсеру'),
      sg.Frame(layout=[[sg.Radio('1', 'rad3', default=True, key='1'),  sg.Radio('0', 'rad3')]],
      title='Оберіть мітку сегмента')
    ],
    [
      sg.Frame(layout=[[sg.Text('Filepath'), sg.InputText(key='filepath'), sg.FileBrowse('Обрати...')
     ]], title='Ведіть параметри для джерела тексту', key='docxParams', visible = True)
    ],
    [
      sg.Frame(layout=[[sg.Text('URL'), sg.InputText(key='url')],
      [sg.Text('ID/class'), sg.InputText(key='select'), sg.Frame(layout=[[sg.Radio('id', 'rad4', default=True, key='id'),  sg.Radio('class', 'rad4')]],
      title='Оберіть ідентифікатор блоку'),]], 
        title='Ведіть параметри для джерела тексту', key='webParams', visible = False)
    ],
    [sg.Output(size=(88, 20), key='result')],
    [sg.Text('Output filename'), sg.InputText(key='output')],
    [sg.Button('Відпарсити текст'), sg.Submit('Записати до CSV')]
]
window = sg.Window('Парсер тексту', layout, resizable=False)

## Array for saving text to csv
## Problem to solve:
# 2. RegExp for nonUnicode chars
textArr = []
try:
  while True:
      event, values = window.read()
      lng = 0 if values['ua'] else 1
      parsType = 0 if values['web'] else 1
      dataType = 1 if values['1'] else 0
      webSelect = 0 if values['id'] else 1
      if event in (None, 'Exit', 'Cancel'):
          break
      if event == 'web':
        window['docxParams'].update(visible = False)
        window['webParams'].update(visible = True)
      if event == 'docx':
        window['docxParams'].update(visible = True)
        window['webParams'].update(visible = False)
      if event == 'Відпарсити текст':
        if parsType == 0:
          pageText = utils.getPageText(values['url'], values['select'], webSelect)
          arrWeb = utils.parseText(pageText, lng)
          textArr.extend(arrWeb)
          values['result'] = ''
          for i in textArr:
            print(i)
        elif parsType == 1:
          docxText = utils.getDocxText(values['filepath'])
          arrDoc = utils.parseText(docxText, lng)
          textArr.extend(arrDoc)
          values['result'] = ''
          for i in textArr:
            print(i)

      if event == 'Записати до CSV':
        filename = values['output'] + '.csv' if(values['output']) else 'results.csv'
        if parsType == 1:
          docxText = utils.getDocxText(values['filepath'])
          arrDoc = utils.parseText(docxText, lng)
          utils.writeToCsv(arrDoc, lng, filename, dataType)
          sg.Popup("Данні збережено до файлу під назвою - " + filename)
        elif len(textArr) > 0:
          utils.writeToCsv(textArr, lng, filename, dataType)
          sg.Popup("Данні збережено до файлу під назвою - " + filename)
except Exception as e:
    sg.popup_error_with_traceback(f'Сталась помилка програми, деталі дивіться нижче:', e)

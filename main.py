import utils
import PySimpleGUI as sg

sg.theme("DarkBlue")

layout = [
    [
      sg.Frame(layout=[[sg.Radio('Укр', 'rad1', key='ua'),  sg.Radio('Англ', 'rad1', default=True)]],
      title='Оберіть мову', key='testKey'),
      sg.Frame(layout=[[sg.Radio('Web', 'rad2', default=True, key='web', enable_events=True),  sg.Radio('Docx', 'rad2', key='docx', enable_events=True)]],
      title='Оберіть тип парсеру'),
      sg.Frame(layout=[[sg.Radio('1', 'rad3', default=True, key='1'),  sg.Radio('0', 'rad3')]],
      title='Оберіть мітку сегмента')
    ],
    [sg.Text('URL'), sg.InputText(key='url', disabled=False)],
    [sg.Text('ID/class'), sg.InputText(key='select', disabled=False), sg.Frame(layout=[[sg.Radio('id', 'rad4', default=True, key='id'),  sg.Radio('class', 'rad4')]],
      title='Оберіть ідентифікатор блоку'),],
    [sg.Text('Filepath'), sg.InputText(key='filepath', disabled=False), sg.FileBrowse('Обрати...')
     ],
    [sg.Output(size=(88, 20), key='result')],
    [sg.Text('Output filename'), sg.InputText(key='output')],
    [sg.Button('Відпарсити текст'), sg.Submit('Записати до CSV')]
]
window = sg.Window('Парсер тексту', layout, resizable=True)
textArr = []
while True:
    event, values = window.read()
    lng = 0 if values['ua'] else 1
    parsType = 0 if values['web'] else 1
    dataType = 1 if values['1'] else 0
    webSelect = 0 if values['id'] else 1
    if event in (None, 'Exit', 'Cancel'):
        break
    if event == 'web':
      window['filepath'].Update(disabled = True)
      window['url'].Update(disabled = False)
      window['select'].Update(disabled = False)
    if event == 'docx':
      window['testKey'].hide_row()
      window['filepath'].Update(disabled = False)
      window['url'].Update(disabled = True)
      window['select'].Update(disabled = True)
    if event == 'Відпарсити текст':
      if parsType == 0:
        test = utils.getPageText(values['url'], values['select'], webSelect)
        arrWeb = utils.parseText(test)
        textArr.extend(arrWeb)
        values['result'] = ''
        for i in textArr:
          print(i)
      elif parsType == 1:
        docxText = utils.getDocxText(values['filepath'])
        arrDoc = utils.parseText(docxText)
        textArr.extend(arrDoc)
        values['result'] = ''
        for i in textArr:
          print(i)

    if event == 'Записати до CSV':
      if parsType == 1:
        docxText = utils.getDocxText(values['filepath'])
        arrDoc = utils.parseText(docxText)
        utils.writeToCsv(arrDoc, lng, values['output'])
      elif len(textArr) > 0:
        utils.writeToCsv(textArr, lng, values['output'])

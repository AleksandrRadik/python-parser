import utils
import PySimpleGUI as sg

layout = [
    [
      sg.Frame(layout=[[sg.Radio('Укр', 'rad1', key='ua'),  sg.Radio('Англ', 'rad1', default=True)]],
      title='Оберіть мову',title_color='red'),
      sg.Frame(layout=[[sg.Radio('Web', 'rad2', default=True, key='web'),  sg.Radio('Docx', 'rad2')]],
      title='Оберіть тип парсеру',title_color='red'),
      sg.Frame(layout=[[sg.Radio('1', 'rad3', default=True, key='1'),  sg.Radio('0', 'rad3')]],
      title='Оберіть тип даних',title_color='red')
    ],
    [sg.Text('URL'), sg.InputText(key='url')],
    [sg.Text('ID/class'), sg.InputText(key='select'), sg.Frame(layout=[[sg.Radio('id', 'rad4', default=True, key='id'),  sg.Radio('class', 'rad4')]],
      title='Оберіть ідентифікатор блоку',title_color='red'),],
    [sg.Text('Filepath'), sg.InputText(key='filepath'), sg.FileBrowse('Обрати...')
     ],
    [sg.Output(size=(88, 20), key='result')],
    [sg.Text('Output filename'), sg.InputText(key='output')],
    [sg.Button('Відпарсити текст'), sg.Submit('Записати до CSV')]
]
window = sg.Window('Парсер тексту', layout)
textArr = []
while True:
    event, values = window.read()
    lng = 0 if values['ua'] else 1
    parsType = 0 if values['web'] else 1
    dataType = 1 if values['1'] else 0
    webSelect = 0 if values['id'] else 1
    if event in (None, 'Exit', 'Cancel'):
        break
    if event == 'Відпарсити текст':
      if parsType == 0:
        test = utils.getPageText(values['url'], values['select'], webSelect)
        textArr = utils.parseText(test)
        for i in textArr:
          print(i)
      elif parsType == 1:
        docxText = utils.getDocxText(values['filepath'])
        arrDoc = utils.parseText(docxText)
        textArr.append(arrDoc)
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

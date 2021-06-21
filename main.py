import utils
import PySimpleGUI as sg

layout = [
    [
      sg.Frame(layout=[[sg.Radio('Укр', 'rad1', key='ua', background_color='gray'),  sg.Radio('Англ', 'rad1', default=True, background_color='gray')]],
      title='Оберіть мову',title_color='pink', background_color='gray'),
      sg.Frame(layout=[[sg.Radio('Web', 'rad2', default=True, key='web', background_color='gray'),  sg.Radio('Docx', 'rad2', background_color='gray')]],
      title='Оберіть тип парсеру',title_color='pink', background_color='gray'),
      sg.Frame(layout=[[sg.Radio('1', 'rad3', default=True, key='1', background_color='gray'),  sg.Radio('0', 'rad3', background_color='gray')]],
      title='Оберіть мітку сегмента',title_color='pink', background_color='gray')
    ],
    [sg.Text('URL', background_color='gray'), sg.InputText(key='url')],
    [sg.Text('ID/class', background_color='gray'), sg.InputText(key='select'), sg.Frame(layout=[[sg.Radio('id', 'rad4', default=True, key='id', background_color='gray'),  sg.Radio('class', 'rad4', background_color='gray')]],
      title='Оберіть ідентифікатор блоку',title_color='pink', background_color='gray'),],
    [sg.Text('Filepath', background_color='gray'), sg.InputText(key='filepath'), sg.FileBrowse('Обрати...')
     ],
    [sg.Output(size=(88, 20), key='result')],
    [sg.Text('Output filename', background_color='gray'), sg.InputText(key='output')],
    [sg.Button('Відпарсити текст'), sg.Submit('Записати до CSV')]
]
window = sg.Window('Парсер тексту', layout, background_color='gray', resizable=True)
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
        arrWeb = utils.parseText(test)
        textArr.append(arrWeb)
        values['result'] = ''
        for i in textArr:
          print(i)
      elif parsType == 1:
        docxText = utils.getDocxText(values['filepath'])
        arrDoc = utils.parseText(docxText)
        textArr.append(arrDoc)
        values['result'] = ''
        for i in textArr[0]:
          print(i)

    if event == 'Записати до CSV':
      if parsType == 1:
        docxText = utils.getDocxText(values['filepath'])
        arrDoc = utils.parseText(docxText)
        utils.writeToCsv(arrDoc, lng, values['output'])
      elif len(textArr) > 0:
        utils.writeToCsv(textArr, lng, values['output'])

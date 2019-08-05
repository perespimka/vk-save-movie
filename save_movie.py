import lxml.html
import requests
import re
from os import getcwd
from sys import stdout
from my_token import login, password
#import getpass



url = 'https://vk.com/'

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Language':'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
'Accept-Encoding':'gzip, deflate',
'Connection':'keep-alive',
'DNT':'1'
}


def get_page(login, password, url): # Логин, возвращает объект сессии ВК

    session = requests.session()
    data = session.get(url, headers=headers)
    page = lxml.html.fromstring(data.content)

    form = page.forms[0]
    form.fields['email'] = login
    form.fields['pass'] = password

    response = session.post(form.action, data=form.form_values())
    print('VK Login: ' + str('onLoginDone' in response.text))
    #response = session.get(url2)
    return session


def search_re(text): # Возвращаем чистую ссылку на видео. Если не найден видос в формате 1080 или 720 возвращает нан
    pattern1 = r'"url1080":"https:\\/\\/(.+?\.1080\.mp4)'
    pattern2 = r'"url720":"https:\\/\\/(.+?\.720\.mp4)'
    foo = re.search(pattern1, text)
    if foo:
        res = re.sub(r'\\', '', foo.group(1))
        return 'https://' + res 
    else:
        foo = re.search(pattern2, text)
        if foo:
            res = re.sub(r'\\', '', foo.group(1))
            return 'https://' + res 
        else:
            return None

url2 = input('Вставьте "Ссылку на видео":')
session = get_page(login, password, url)
r = session.get(url2, headers=headers)

dir_url = search_re(r.text) # Получаем прямую ссылку на видео
print('Прямая ссылка на видео: ' + dir_url)

video = session.get(dir_url,stream=True) # Сохраняем видео 
file_length = round (int(video.headers['content-length']) / 1000000, 2)
print('Размер файла: ' + str(file_length) + ' mb')
print('Качаем видео...')
chunk_size = int(video.headers['content-length']) // 100
proc = 0
fname = dir_url.split('/')[-1]
with open (fname, 'wb') as f:
    for chunk in video.iter_content(chunk_size):
        f.write(chunk)
        if proc < 100:
            proc += 1
            stdout.write('Скачано %d%% \r' % proc)
            stdout.flush()
print('Файл ' + fname + ' сохранен в: ' + getcwd())

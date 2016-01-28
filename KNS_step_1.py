import urllib.request as urlr
import re
import codecs


def contents(index_url):
    result = []
    print ('Downloading table of content', end='...')
    index_page = urlr.urlopen('http://'+ index_url)
    index_text = index_page.read().decode(u'utf-8')
    m = re.findall(u'/ru/Artists/ru[\w-]+\.html', index_text)
    for x in m:
        result.append(x)
        index_page = urlr.urlopen('http://' + index_url + x)
        index_text = index_page.read().decode(u'utf-8')
        n = re.findall(x[0:-5] + u'-p\d+\.html', index_text)
        result += n
    print(str(len(result)) + ' ' + 'references')
    return result

def href_list(index_url, path):
    result = []
    index_page = urlr.urlopen('http://' + index_url + path)
    index_text = index_page.read().decode(u'utf-8')
    m = re.findall(u'(?<=<a href=\")[./\w-]+(?=\" title=\")', index_text)
    for x in m:
        result.append(x)
        index_page = urlr.urlopen('http://' + index_url + x)
        index_text = index_page.read().decode(u'utf-8')
        n = re.findall(x + u'index-p\d+\.html', index_text)
        result += n
    return result

def get_text(address):
    text_page = urlr.urlopen('http://' + address)
    text = text_page.read().decode(u'utf-8')
    m = re.search(u'(?<=<h1>)(.+)+(?=</h1>)', text)
    title = m.group(0)
    title = re.sub(u'<br />Текст песни ', '\n', title) + '\n'*2
    m = re.search(u'(?<=<p id=\"textpesni\">\\n)(.+\\n)+(?=\\n*</p>)', text)
    song_text = m.group(0)
    song_text = re.sub(u'<br>', '', song_text)
    song_text = re.sub(u'&quot;', '"', song_text)
    song_text = re.sub(u'&#39;', "'", song_text)
    return title + song_text + '\n'

def crawler(N, file='song_text.txt', index_url='lyricshare.net'):
    count = 1
    print (u'Downloading from ... www.' + index_url)
    cont_table = contents(index_url)
    with open(file, 'w') as fw:
        for x in cont_table:
            artist = href_list(index_url, x)
            for hr in artist:
                print (u'Downloading ... ' + hr, end=' ... ')
                text_ref = href_list(index_url, hr)
                print (str(len(text_ref)) + ' references')
                for tr in text_ref:
                    text = get_text(index_url + tr)
                    ru_letters = len(re.findall(u'[А-Яа-я]', text))
                    en_letters = len(re.findall(u'[A-Za-z]', text))
                    if ru_letters > en_letters:
                        fw.write(text)
                        count +=1
                    if count > N:
                        print (str(count - 1) + u' songs texts downloaded')
                        return count
    print (str(count - 1) + u' songs texts downloaded')
    return count

t = crawler(10000)

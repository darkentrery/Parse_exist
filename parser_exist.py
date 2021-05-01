import requests, re
from bs4 import BeautifulSoup as BS

user_agent = ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36')
brend, articul = ('DENSO', 'CTR'), ('k16r-u11', 'CBM-23R')

def find_pid(brend, articul):
    url = 'https://www.exist.ru/Price/?pcode=' + str(articul)
    html = requests.get(url, user_agent)
    soup = BS(html.content, 'html.parser')
    data_brend = soup.find_all('ul', class_="catalogs")
    data_pid = data_brend[0].find_all('a')
    for i in range(len(data_pid)):
        pid = data_pid[i]['href'][12:]
        brend_web = data_pid[i].b.text
        if brend.lower() == brend_web.lower():
            PID = pid
            break
    data_brend = data_brend[0].b#find_all('b')
    textlookfor = r'pid=[^"]{0,}'
    #for i in range(len(data_brend)):
    #    pid = re.findall(textlookfor, str(data_pid[i]))
    #    print(pid)
    return PID

def parse_articul(url):
    url = 'https://www.exist.ru' + str(url)
    html = requests.get(url, user_agent)
    soup = BS(html.content, 'html.parser')
    data_articul = soup.find_all('a', id="ctl00_b_ctl00_hlNotepad")[0]['onclick']
    textlookfor = r"'[^']*'"
    text = re.findall(textlookfor, data_articul)
    text = text[0]
    #print(text)
    return text

def parse_page(pid):
    url = 'https://www.exist.ru/Price/?pid=' + str(pid)
    html = requests.get(url, user_agent)
    soup = BS(html.content, 'html.parser')
    text_java = soup.find_all('form', method="post")[0].script
    textlookfor_P = r'"BlockText":"[^,:/]*"'
    textlookfor_B = r'"CatalogName":"[^,:/]*"'
    textlookfor_A = r'"PartNumber":"[^,:/]*"'
    textlookfor_F = r'"ProdUrl":"[^,:]*"'
    textrename_1 = r'\\u0026'
    textrename_2 = r'Parts.axd'
    text_P = re.findall(textlookfor_P, str(text_java))
    text_B = re.findall(textlookfor_B, str(text_java))
    text_A = re.findall(textlookfor_A, str(text_java))
    text_F = re.findall(textlookfor_F, str(text_java))
    text_f = []
    text_a = []
    for i in range(len(text_F)):
        text_f.append(re.sub(textrename_1, r'&', text_F[i]))
        text_f[i] = re.sub(textrename_2, r'Parts/Float.aspx', text_f[i])[11:len(text_f[i]) - 1]
        text_a.append(parse_articul(text_f[i]))

    data = []
    for i in range(len(text_P)):
        data.append([text_P[i][13:len(text_P[i]) - 1], text_B[i][15:len(text_B[i]) - 1], text_a[i][1:len(text_a[i]) - 1]])
    #text_java = soup.find_all('script', type="text/javascript")
    #print(text_java)
    #print(text_P)
    #print(text_B)
    #print(text_A)
    #print(text_f)
    #print(text_a)
    print(data)


for i in range(2):

    pid = find_pid(brend[i], articul[i])
    parse_page(pid)
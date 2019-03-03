import os
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector

FOLDER = r'D:\TMP\DOWNLOADED_CONTENT\HTML'
list_of_files = ['200711-Aryciskup-na-niedziele.html']
for file in list_of_files:
    path = os.path.join(FOLDER, file)
    with open(path) as f:
        content = f.read()
    #enc = EncodingDetector(content, is_html=True)
    soup = BeautifulSoup(content, 'html.parser')
    #soup = soup.prettify('iso-8859-2')
    #print(soup.original_encoding)
   # print(enc)
    x = soup.find(class_="TytulKomentowanegoWpisu")
    y = soup.find(class_="TrescKomentowanegoWpisu")
    print(y.text.encode('iso-8859-2'))

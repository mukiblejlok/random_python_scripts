import os
import requests
from bs4 import BeautifulSoup


def download_file(remote_path, dest_path):
    # check if file already exists
    if os.path.exists(dest_path):
        return None

    # Download remote data ...
    r = requests.get(remote_path)
    # ... and save it to local destination
    with open(dest_path, 'wb') as wf:
        wf.write(r.content)
    print("{} saved to '{}'".format(remote_path, dest_path))
    return r.content


def save2folder(data, folder, file):
    if not os.path.exists(folder):
        os.makedirs(folder)
    path = os.path.join(folder, file)
    with open(path, 'wb') as wf:
        wf.write(data)


def url_to_filename(url):
    elements = url.split("/")
    filename = "{}{}-{}".format(*elements[-3:])
    return filename


def get_next_html(content):
    NEXT_HTML_ID = 'BlogWpisPoprzedniLewy'
    PREV_HTML_ID = 'BlogWpisNastepnyPrawy'
    try:
        soup = BeautifulSoup(content, 'html.parser')
        next_div = soup.find(id=PREV_HTML_ID)
        next_href = (next_div.find_all('a')[0].get('href'))
        return next_href
    except:
        return None


if __name__ == '__main__':
    BASE_URL = r'http://wo.blox.pl'
    FIRST_URL = r'/2006/08/Zielono-na-czarnym.html'
    SAVE_FOLDER = r"D:\TMP\DOWNLOADED_CONTENT"
    html_folder = os.path.join(SAVE_FOLDER, "HTML2")
    rss_folder = os.path.join(SAVE_FOLDER, "RSS2")

    html_url = "{}{}".format(BASE_URL, FIRST_URL)
    while html_url:
        html_file = url_to_filename(html_url)
        rss_file = html_file.replace(".html", ".rss")
        rss_url = html_url.replace(".html", ".rss")

        # Download HTML File
        html_req = requests.get(html_url)
        html_req.encoding = 'iso-8859-2'
        html_content = html_req.content
        print("Downloaded: {}".format(html_url))

        # Save HTML File
        save2folder(html_content, html_folder, html_file)

        # Download RSS File
        rss_content = requests.get(rss_url).content
        # Save RSS File
        save2folder(rss_content, rss_folder, rss_file)

        # Get next HTML to download
        html_url = get_next_html(html_content)
        if html_url is not None:
            html_url = "{}{}".format(BASE_URL, html_url)

"""
Download information about the PACKT books.

*Ths doesn't work any more.
"""
import os
import shutil, json
import requests
from bs4 import BeautifulSoup


headers = {
    "Host": "www.packtpub.com",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
}

def main():
    tops = set()
    pairs = {}
    content = 'content'
    for top, dirs, files in os.walk(content):

        for folder in dirs:
            root = os.path.join(content, folder)
            cpath = os.path.join(root, 'info.json')
            with open(cpath, 'r') as stream:
                data = json.load(stream)
            update(data, folder)
            with open(cpath, 'w') as stream:
                json.dump(data, stream, indent=4)


from lxml import etree
from io import StringIO

import gzip
import zlib
def update(data, folder):

    if ('url' in data) is False:
        print('no url for', folder)
        return

    url = data['url']
    req = requests.get(url, headers=headers)
    if req.status_code == 200:
        print('Success request.', req, url)
    else:
        print('Failure to call', url, req.status_code)
        print(req.reason)
        return

    html_doc = req.text
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(html_doc), parser)

    title_el =  tree.xpath('//*[@id="mobile-book-container"]/div[2]/div[1]/h1')
    caption_el = tree.xpath('//*[@id="mobile-book-container"]/div[2]/div[3]')
    img_el = tree.xpath('//*[@id="mobile-book-container"]/div[1]/div[1]/span/a/img')
    desc_el = tree.xpath('//*[@id="main-book"]/div[2]/div/div[2]/div/div')
    isbn_13 = tree.xpath('//*[@id="main-book"]/div[2]/div/div[1]/div/div[1]/span[2]')


    title = title_el[0].text if len(title_el) > 0 else 'No Title'
    caption = caption_el[0].text if len(caption_el) > 0 else 'No Caption'
    img = img_el[0].get('src') if len(img_el) > 0 else 'No Image'
    desc_item = desc_el[0] if len(desc_el) > 0 else 'No Desc'
    isbn = isbn_13[0].text if len(isbn_13) > 0 else 'ISBN'
    # result = etree.tostring(tree.getroot(), pretty_print=True, method="html")
    import pdb; pdb.set_trace()  # breakpoint a9cfa2d4 //
    desc_soup = BeautifulSoup(etree.tostring(desc_item, method='html'), 'html.parser')
    desc = desc_soup.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    alt_title = soup.title.string

    content = dict(
        title=title,
        caption=caption,
        img=img,
        isbn=isbn,
        desc=desc,
        alt_title=alt_title,
    )
    data.update(content)


if __name__ == '__main__':
    main()

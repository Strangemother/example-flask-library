"""
open the 'info.json' in each sub folder of the 'content' directory.
Read the 'img' field and download (if required).
Write the new image file to the same directory as "image.xxx".
"""
import os
import shutil, json
import requests

def main():
    tops = set()
    pairs = {}
    content = 'content'
    for top, dirs, files in os.walk(content):

        for folder in dirs:
            root = os.path.join(content, folder)
            cpath = os.path.join(root, 'info.json')
            if os.path.exists(cpath) is False:
                print('!Cannot find', cpath)
                continue

            with open(cpath, 'r') as stream:
                data = json.load(stream)
            update(data, root)
            with open(cpath, 'w') as stream:
                json.dump(data, stream, indent=4)


def update(data, root):

    url = data.get('img', None)
    if url is None:
        print('Does not have image:', data.get('title', url))
        return
    path, ext = os.path.splitext(url)
    name = 'image{}'.format(ext)
    path = os.path.join(root, name)
    data['image'] = path
    if os.path.exists(path):
        print('Image exists; exiting.')
        return

    print('Downloading', url)
    req = requests.get(url)
    print('Result:', req)

    if req.status_code == 200:
        print('Creating image', path)
        stream = open(path,'wb')
        stream.write(req.content)
        stream.close()

if __name__ == '__main__':
    main()

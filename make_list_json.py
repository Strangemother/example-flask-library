"""
Move all the top level files into a folder of the same name.
"""
import os
import shutil, json

def main():
    tops = set()
    pairs = {}
    content = 'content'
    res = []
    items_path = os.path.join(content, 'item.json')

    for top, dirs, files in os.walk(content):
        for folder in dirs:
            root = os.path.join(content, folder)
            data = get_data(root)
            if data is None:
                print('Bad item', root)
                continue

            if 'supplement' in data:
                # expand supplement items
                for sup in data['supplement']:
                    sup_path = os.path.join(root, sup)
                    sup_data = get_data(sup_path)
                    data[sup] = sup_data
            update(data, folder)
            res.append(data)

    with open(items_path, 'w') as stream:
        json.dump(res, stream, indent=4)

def get_data(path):
    cpath = os.path.join(path, 'info.json')
    if os.path.exists(cpath):
        with open(cpath, 'r') as stream:
            return json.load(stream)
    else:
        print('Cannot load', path)
    return None

def update(data, folder):
    if 'url' in data:
        print('Current Folder: "{}" URL: {}'.format(folder, data['url']))

if __name__ == '__main__':
    main()

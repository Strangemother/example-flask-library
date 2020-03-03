"""
Move all the top level files into a folder of the same name.
"""
import os
import shutil, json

def main():
    tops = set()
    pairs = {}
    content = 'content'
    for top, dirs, files in os.walk(content):

        for folder in dirs:
            root = os.path.join(content, folder)
            cpath = os.path.join(root, 'info.json')
            data = None
            if os.path.exists(cpath):
                with open(cpath, 'r') as stream:
                    data = json.load(stream)
            else:
                print('No data for', folder)
                print('Content', cpath, 'is missing')
                continue

            supname = '{}_supplement'.format(folder)
            if supname in dirs:
                print('found sibling', folder)
                shutil.move(os.path.join(content, supname), root)
                if ('supplement' in data) is False:
                    data['supplement'] = []
                data['supplement'].append(supname)
            update(data, folder, dirs)
            if data is not None:
                with open(cpath, 'w') as stream:
                    json.dump(data, stream, indent=4)


def update(data, folder, dirs):
    data['name'] = folder
    if 'url' in data:
        print('Current URL: {}'.format(data['url']))
        return
    url = input('URL for "{}".\n Leave blank for no change'.format(folder))
    if len(url) > 0:
        data['url'] = url
    else:
        print('No change.')

if __name__ == '__main__':
    main()

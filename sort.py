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
        for filepath in files:
            path, fne = os.path.split(filepath)
            fn, ext = os.path.splitext(fne)
            tops.add(fn)
            if (fn in pairs) is False:
                pairs[fn] = ()
            pairs[fn] += (os.path.join(top, filepath), )


    for folder in tops:
        root = os.path.join(content, folder, )
        os.makedirs(root)
        files = pairs.get(folder, ())
        for filepath in files:
            old = filepath
            path, fne = os.path.split(filepath)
            new_loc = os.path.join(root, fne)
            print('Moving', old, new_loc)
            shutil.move(old, new_loc)
        data = dict(
            root=root,
            files=files,
            )
        cpath = os.path.join(root, 'info.json')
        with open(cpath, 'w') as stream:
            json.dump(data, stream)


if __name__ == '__main__':
    main()

import os
import shutil


def main():
    """
    Files are listed flat; with the same name but different extension

    get the file list within content-2 and move all files into
    sub folders of the same name.

    """
    files = os.listdir('content-2')
    res = set()

    for name in files:
        res.add(os.path.splitext(name)[0])
    print(res)

    for name in res:
        dp = os.path.join('content-2', name)
        if os.path.isdir(dp):
            continue
        os.mkdir(dp)
        for filename in files:
            fp = os.path.join('content-2', filename)
            if filename.startswith(name):
                mfp = os.path.join('content-2', name)
                shutil.move(fp, mfp)

if __name__ == '__main__':
    main()

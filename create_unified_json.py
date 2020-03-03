import shutil
"""
Get all the JSONS for all the books and produce one large readable json.
"""
from books import *
from get_meta import create_json
import json


def create_path(name, subdir=''):
    nospace = name.replace(' ', '_')
    subpath = os.path.join('jsons', subdir)
    return os.path.join(subpath, f'{nospace}.json')

import os
import requests


def main():
    refactor_organise()
    combine()


def refactor_organise():
    create_one()
    # oops_correct_ext_names()
    # rename_files()
    # res = infos()
    # update_cleans(res)
    # update_roots()
    update_images()
    #update_files()
    # move_images()


def combine():

    subdir = 'jsons/clean'
    res = ()

    img_files = os.listdir('jsons/images')
    imgm = {}
    for img in img_files:
        rp, fn = os.path.split(img)
        rf, ext = os.path.splitext(fn)
        imgm[rf] = img

    for item in os.listdir(subdir):
        content = get_json(subdir, item)
        content['image'] = imgm.get(content['isbn'])
        res += (content, )
    write_json('jsons/output.json', res)
    return res


def move_images(dirpath='content'):
    """
    move a 'image.xxx' from the content subdirectory to the json/images
    folder.
    """
    res = ()
    dirs = os.listdir('content')
    for item in dirs:

        subdir = os.path.join('content', item, )
        if os.path.isfile(subdir):
            print('Skipping', subdir)
            continue

        files = os.listdir(subdir)
        for fn in files:
            full_fn = os.path.join(subdir, fn)
            path, filename = os.path.split(fn)
            name, ext = os.path.splitext(filename)
            info = os.path.join(subdir, 'info.json')
            isbn = None
            if os.path.isfile(info):
                content = get_json(info)
                isbn = content.get('isbn')
            if name == 'image':
                print('Found an image', isbn)
                new_fn = os.path.join('jsons', 'images', f'{isbn}{ext}')
                if os.path.exists(new_fn):
                    print('Dest already exists', isbn, subdir)
                    continue

                os.rename(full_fn, new_fn)

    return res


def update_images(dirpath='jsons/clean'):
    """
    iterate all files within the given dirpath.
    If the 'image' attr exists, download the image and store in
    jsons/images as ISBN.ext.

    Do not perform if the target file already exists.
    """
    files = os.listdir(dirpath)
    for filename in files:
        content = get_json(dirpath, filename)

        #if content.get('image') is None:
        # System applied image is None.
        name = content.get('asset', None)
        # no asset - no data exists.
        if name is None:
            continue

        print(f'resolving "{name}"')
        # Get image list
        imgs = content['images']

        # download the image
        url = imgs.get('image')
        if url is None:
            print('using google thumbnail image')
            url = imgs.get('thumbnail')

        # save in image folder as ISBN.ext
        if url is None:
            continue

        _, ext = os.path.splitext(url)
        if len(ext) == 0:
            ext = '.jpg'
        imgname = f'{content["isbn"]}{ext}'
        img = os.path.join('jsons', 'images', imgname)
        # Download if missing.
        if os.path.exists(img) is False:
            download_image(url, img)
        content['image'] = imgname
        write_json(os.path.join(dirpath, filename), content)

def download_image(url, path):
    response = requests.get(url, stream=True)
    print('Downloading', url)
    with open(path, 'wb') as stream:
        shutil.copyfileobj(response.raw, stream)
        return True
    return False


def update_files():
    """Iteral all clean jsons and ensure the files param
    """
    subdir = 'jsons/clean'
    missed = ()

    for item in os.listdir(subdir):
        content = get_json(subdir, item)
        files = content.get('files')
        if len(files) == 0:
            print('file assocation: ', content.get('asset'))
            root = content['root']
            dir_files = os.listdir(root)
        else:
            dir_files = []
            for fn in files:
                name = fn
                if fn.startswith('content'):
                    _, name = os.path.split(fn)
                dir_files.append(name)
        content['files'] = dir_files
        write_json(os.path.join(subdir, item), content)


    print('missed', len(missed), missed)


def update_roots():
    """Iteral all clean jsons and ensure the 'root' param
    """
    subdir = 'jsons/clean'
    missed = ()

    for item in os.listdir(subdir):
        content = get_json(subdir, item)
        root = content.get('root')
        if root is None:
            print('Rooting: ', content.get('asset'))
            nospace = content['asset'].replace(' ', '')

            dirpath = os.path.join('content', nospace)
            if os.path.isdir(dirpath):
                content['root'] = dirpath
                print('  ', dirpath)
            else:
                print('No found', nospace)
                missed += (item,)
                newname = input('provide subpath:')
                dirpath = os.path.join('content', newname)
                content['root'] = dirpath
            write_json(os.path.join(subdir, item), content)

    print('missed', len(missed), missed)


def update_cleans(res):
    """
    Merge all info.json dict items into the ISBN.json within the clean
    directory.
    This merges image and files dict.
    """

    for isbn, info in res:
        path = os.path.join('jsons', 'clean', f'{isbn}.json')

        if os.path.exists(path) is False:
            print('No association for', isbn)
            continue

        print(path)
        with open(path, encoding='utf') as stream:
            content = json.load(stream)

        content['url'] = info['url']
        content['image'] = info['image']
        content['files'] = info['files']
        content['root'] = info['root']
        write_json(path, content)


def write_json(path, content):
    with open(path, 'w', encoding='utf') as stream:
        json.dump(content, stream, indent=4)


def get_json(*path):
    path = os.path.join(*path)
    with open(path, encoding='utf') as stream:
        return json.load(stream)


def infos(filename='info.json'):
    """Fetch all info files from every subdir within the content.
    return a tuple of dicts
    """
    res = ()
    dirs = os.listdir('content')
    for item in dirs:
        info = os.path.join('content', item, filename)
        if os.path.exists(info):
            print('found', info)
            with open(info, encoding='utf') as stream:
                data = json.load(stream)
                res += ((data.get('isbn'), data,),)
        else:
            print('Not found', info)
    return res


def create_one():

    for isbn, name in all_books:
        gc = get_content('google', isbn)
        ic = get_content('isbndb', isbn)
        if gc is False or ic is False:
            print('Failure for', name)

        book = create_book(gc, ic, name)
        create_json(book, isbn, 'clean')


class Struct(object):

    def __init__(self, **item):
        self.__dict__.update(**item)

    def __getattr__(self, k):
        if k in self.__dict__:
            return self.__dict__[k]
        print(f'{self} has no key', k)
        return None

    def __setattr__(self, k, v):
        self.__dict__[k] = v


class Google(Struct):
    pass

class ISBN_DB(Struct):
    pass



def create_book(google_content, isbndb_content, name):
    gc = google_content['volumeInfo'] if google_content is not False else {}
    ic = isbndb_content['book'] if isbndb_content is not False else {}
    gc, ic = Google(**gc), ISBN_DB(**ic)
    res = Struct(asset=name)
    get_pages(res, gc, ic)
    get_titles(res, gc, ic)
    get_isbn(res, gc, ic)
    get_authors(res, gc, ic)
    get_publisher(res, gc, ic)
    get_categories(res, gc, ic)
    get_version(res, gc, ic)
    get_rating(res, gc, ic)
    get_images(res, gc, ic)
    get_cost(res, gc, ic)


    res.publish_date = ic.publish_date or gc.publishedDate
    get_files(res, google_content, isbndb_content)


    return res.__dict__

def get_isbn(res, gc, ic):
    res.isbn = ic.isbn
    res.isbn13 = ic.isbn13


def get_files(res, gc, ic):
    gc = gc or {}
    ic = ic or {}

    res.files = (ic.get('files') or []) + (gc.get('files') or [])


def get_authors(res, gc, ic):
    res.authors = list(set((ic.authors or []) + (gc.authors or [])))


def get_rating(res, gc, ic):
    res.rating = gc.averageRating or -1
    res.rating_count = ic.ratingsCount or -1


def get_images(res, gc, ic):
    images = dict(
        image=ic.image
    )
    images.update(gc.imageLinks or {})
    res.images = images


def get_publisher(res, gc, ic):
    res.publisher = list(filter(None, set([ic.publisher, gc.publisher])))


def get_categories(res, gc, ic):
    res.categories = (ic.subjects or []) + (gc.categories or [])


def get_cost(res, gc, ic):
    res.cost = float(ic.msrp or -1)


def get_version(res, gc, ic):
    version = dict(
        edition=ic.edition,
        version=gc.contentVersion,
    )


def get_titles(res, gc, ic):
    titles = dict(
            title_short=gc.title,
            subtitle=gc.subtitle,
            description=gc.description,

            title_long=ic.title_long,
            synopsys=ic.synopsys,
            title=ic.title,
        )
    res.title = titles


def get_pages(res, gc, ic):
    """
    fill 'res' pages and page_detail with counts.
    """
    pages = ic.pages, gc.pageCount
    sp = tuple(set(pages))
    ps = sp[0]
    res.page_detail = {'count': -1, 'delta': 0}
    if ps is None:
        return

    if pages[0] is None:
        res.page_detail['count'] = res.pages = pages[1]
        return

    if pages[1] is None:
        res.page_detail['count'] = res.pages = pages[0]
        return

    if len(sp) > 1:
        mp = min(pages)
        delta = max(pages) - mp
        res.page_detail = { 'count': mp, 'delta': delta}
        ps = f"{mp} ~ {delta}"
    else:
        res.page_detail['count'] = ps
    res.pages = ps
    return res


def get_content(subdir, isbn):
    path = os.path.join('jsons', subdir, f'{isbn}.json')
    if os.path.exists(path) is False:
        print('Cannot open', subdir, isbn)
        return False

    with open(path, encoding='utf') as stream:
        res = json.load(stream)

    if res is False:
        return False

    #res['files'] = os.listdir(os.path.join('content', subdir))
    return res


def oops_correct_ext_names():
    join = os.path.join
    subdir = 'isbndb'
    for name in os.listdir(join('jsons', subdir)):
        a, b = os.path.splitext(name)
        aa, b = os.path.splitext(a)
        fp = join('jsons', subdir, name)
        nfp = join('jsons', subdir, f'{aa}.json')
        if os.path.exists(nfp):
            continue

        os.rename(fp, nfp)


def rename_files():
    for isbn, name in all_books:
        print('Renaming', name)
        rename('google', name, isbn)
        rename('isbndb', name, isbn)


def rename(subdir, name, isbn):
    """Deprecated. Rename any found json file within the subdiractory and
    rename to ISBN.json if required.
    """
    gp = create_path(name, subdir)
    if os.path.exists(gp):
        new_name = f'{isbn}.json'
        ngp = create_path(new_name, subdir)
        if os.path.exists(ngp):
            print('Exists:', new_name)
        else:
            print(f'  renaming {name} to {new_name}')
            os.rename(gp, ngp)
    else:
        print('  Not found', gp)


if __name__ == '__main__':
    main()

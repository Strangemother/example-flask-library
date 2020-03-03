"""
Fetch inforamation on all the books ISBN from google and isbndb
"""
import os
import requests
import json

ISBNDB_REST_KEY = '43683_79b582d3baa2f23748557e2c3abcf69c'
from books import *


def main():
    # res = get_uninfo(False)
    # res = extract_info_isbns(res)
    get_isbns(isbns + info_isbns)


def extract_info_isbns(items):
    """Extract the ISBN and title from all 'info.json files within the
    content sub directories. Returns a tuple of tuples (ISBN, title)"""
    res = ()
    for item in items:
        fp = os.path.join('content', item, 'info.json')
        with open(fp) as stream:
            content = json.load(stream)
            try:
                res += ((content['isbn'], content['title']),)
            except KeyError:
                print('Cannot access ISBN of', item)
    return res


def get_uninfo(not_infos=False):
    """Return a list of directories from the content folder of which do not
    contain an 'info.json'
    """
    items = os.listdir('content')
    res = ()
    for path in items:
        dp = os.path.join('content', path)
        if os.path.isdir(dp):
            if os.path.exists(os.path.join(dp, 'info.json')) is not_infos:
                continue
            res += (path,)

    return res


def get_isbns(items):
    if os.path.isdir('jsons') is False:
        os.mkdir('jsons')

    for isbn, name in items:
        print('Calling', name)
        g_book = get_google(isbn, name)
        db_book = get_isbndb(isbn, name)


def get_google(isbn, name):
    if exists('google', isbn):
        print('ignoring', name)
        return None
    print('get_google', isbn)
    url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}'
    res = requests.get(url)
    if res.ok:
        content = get_content(res)
        #content = res.json()

        if content is False:
            return None

        if content['totalItems'] == 0:
            print('Nothing found for', isbn, name)
            return None
        book = content['items'][0]
        create_json(book, isbn, 'google')

    return book


def exists(subdir, name):
    path = create_path(name, subdir)
    return os.path.exists(path)


def create_path(name, subdir=''):
    nospace = name.replace(' ', '_')
    subpath = os.path.join('jsons', subdir)
    return os.path.join(subpath, f'{nospace}.json')


def create_json(book, name, subdir=''):
    nospace = name.replace(' ', '_')
    subpath = os.path.join('jsons', subdir)
    if os.path.isdir(subpath) is False:
        os.mkdir(subpath)

    with open(f"{subpath}/{nospace}.json", 'w', encoding='utf') as stream:
        json.dump(book, stream, indent=4)

import requests


def get_isbndb(isbn, name):
    if exists('isbndb', isbn):
        print('ignoring', name)
        return None
    print('get_isbndb', isbn)
    api_url = 'https://api2.isbndb.com/book'
    h = {'Authorization': ISBNDB_REST_KEY}
    resp = requests.get(f"{api_url}/{isbn}", headers=h)
    res = get_content(resp)
    if resp is False:
        return None

    #res = resp.json()
    create_json(res, isbn, 'isbndb')
    return res


def get_content(response):
    if response.ok:
        try:
            return response.json()
        except Exception as exc:
            return False
    return False


if __name__ == '__main__':
    main()


"""


https://openlibrary.org/api/books?bibkeys=ISBN:9781786464392&format=json

978-1-78646-439-2   artificial intelligence with python
978-1-59327-599-0   automate the boring stuff with python
978-1-59327-590-7   blackhat python
978-1-78646-225-1   building restful python webservices
978-1-59327-119-0   code craft
978-1-59327-822-9   cracking codes with python
978-1-59327-640-9   doing math with python
978-1-78588-685-0   expert python programming
978-1-59327-192-3   grayhat python
978-1-59327-890-8   impractical python projects
978-1-59327-795-6   invent your own computer games with python
978-1-78728-537-8   learning concurrency in python
978-1-78528-972-9   mastering python
978-1-78913-599-2   mastering python networking
978-1-59327-867-0   math adventures with python
978-1-59327-857-1   mission python
978-1-59327-857-1   modern python cookbook
978-1-78528-228-7   python data analysis cookbook
978-1-78646-213-8   python data science essentials
978-1-78646-735-5   python data structures and algorithms
978-1-59327-407-8   python for kids 1490905401
978-1-78712-945-0   python gui programming cookbook
978-1-78728-289-6   python high performance
978-1-78355-513-0   python machine learning
978-1-78588-111-4   python microservices development
978-1-59327-604-1   python playground_geeky projects for the curious programmer
978-1-78646-757-7   python programming with raspberrypi
978-1-59327-878-6   serious python
978-1-78646-852-9   software architecture with python
978-1-59327-614-0   teach your kids to code
978-1-78588-677-5   webdevelopment with django cookbook
"""

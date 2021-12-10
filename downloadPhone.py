# download photos from the phone with HTTP server. 

# HOST = 'http://192.168.0.173:7666'
HOST = 'http://10.209.115.209:7666'
PATH = '/DCIM/OpenCamera'
DEST = 'heavy'
# DEST = '/Volumes/TOSHIBA EXT/!2021'
LEFT = "<a href='"
RIGHT = "'>"

from requests import get
import os
from os import path
from datetime import datetime
from jdt import Jdt

def main():
    res = get(HOST + PATH)
    os.chdir(DEST)
    dir_name = datetime.today().strftime('%Y-%m-%d')
    os.mkdir(dir_name)
    os.chdir(dir_name)
    parts = res.text.split(LEFT)[1:]
    with Jdt(len(parts), 'Downloading') as j:
        for part in parts:
            fullname = part.split(RIGHT, 1)[0]
            _, filename = path.split(fullname)
            try:
                if filename == '..':
                    continue
                # print(filename)
                if path.isfile(filename):
                    print(filename, 'already here. ')
                    continue
                res = get(HOST + fullname)
                with open(filename, 'wb') as f:
                    f.write(res.content)
            finally:
                j.acc()
    input('Done! Enter...')

main()

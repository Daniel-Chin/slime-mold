# download photos from the phone with HTTP server. 

# HOST = 'http://192.168.0.173:7666'
HOST = 'http://10.209.93.1:7666'
PATH = '/DCIM/OpenCamera'
LEFT = "<a href='"
RIGHT = "'>"

from requests import get
import os
from os import path
from datetime import datetime
from jdt import Jdt

def main():
    res = get(HOST + PATH)
    os.chdir('heavy')
    dir_name = datetime.today().strftime('%Y-%m-%d')
    os.mkdir(dir_name)
    os.chdir(dir_name)
    parts = res.text.split(LEFT)[1:]
    with Jdt(len(parts), 'Downloading') as j:
        for part in parts:
            fullname = part.split(RIGHT, 1)[0]
            _, filename = path.split(fullname)
            if filename == '..':
                j.acc()
                continue
            # print(filename)
            res = get(HOST + fullname)
            with open(filename, 'wb') as f:
                f.write(res.content)
            j.acc()
    input('Done! Enter...')

main()

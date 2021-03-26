#!/usr/bin/env python3

import os
from jdt import Jdt
from os.path import splitext, dirname, isdir, join, \
    basename, abspath

def main():
    folder = input('Drag folder/photo here and press Enter: ')
    if not isdir(folder):
        os.chdir(dirname(folder))
    os.chdir(folder)
    files = os.listdir()
    files.sort()
    n = len(files)
    assert 'y' == input(
        f'There are {n} files here. Proceed? y/n > '
    ).lower()
    with Jdt(n) as j:
        for i, fn in enumerate(files):
            _, ext = splitext(fn)
            os.rename(fn, f'{i}{ext}')
            j.acc()
    print('Rename complete. ')
    os.chdir(folder)
    base = basename(folder)
    # ffmpeg = join(dirname(__file__), "ffmpeg")
    ffmpeg = "ffmpeg"
    command = f'{ffmpeg} -r 30 -i %d.jpg ../{base}.mp4'
    print(command)
    os.system(command)
    print('Success.')

main()

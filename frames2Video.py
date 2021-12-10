#!/usr/bin/env python3

import os
from jdt import Jdt
from os.path import splitext, dirname, isdir, join, \
    basename, abspath

# FFMPEG = 'ffmpeg'
FFMPEG = '~/Downloads/ffmpeg'
EXT = '.jpg'

def main():
    folder = input('Drag folder/photo here and press Enter: ')
    folder = folder.replace('\\', '').rstrip(' ')
    if not isdir(folder):
        os.chdir(dirname(folder))
    os.chdir(folder)
    files = os.listdir()
    files.sort()
    n = len(files)
    assert 'y' == input(
        f'There are {n} files here. Proceed? y/n > '
    ).lower()
    dest_names = []
    for i, fn in enumerate(files):
        _, ext = splitext(fn)
        assert ext.lower() == EXT
        dest_names.append(f'{i}{ext}')
    if set(files).intersection(dest_names):
        if set(files) == set(dest_names):
            print('Already did rename. Skipping. ')
        else:
            print('Unexpected scenario 3489pfweah3tqp2h53tp')
    else:
        with Jdt(n) as j:
            for fn, dest in zip(files, dest_names):
                os.rename(fn, dest)
                j.acc()
        print('Rename complete. ')
    os.chdir(folder)
    base = basename(folder)
    command = f'{FFMPEG} -r 30 -i %d.{ext} ../{base}.mp4'
    print(command)
    os.system(command)
    print('Success.')

main()

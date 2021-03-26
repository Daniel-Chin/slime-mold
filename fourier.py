print('loading...')
from PIL import Image, ImageDraw
import numpy as np
import os
from jdt import Jdt
from console import console
from datetime import datetime
from interactive import inputChin

TIME_FLUCT_TOLERANCE = .2

def main():
    folder = chooseFolder()
    duration_of_interest = chooseDurationOfInterest(folder)
    region_of_interest = chooseRegionOfInterest(folder, duration_of_interest)
    frames = getListOfFrames(folder, duration_of_interest, region_of_interest)
    print('Doing rfft...')
    f = np.fft.rfft(frames, axis = 0)
    temp = present(f)
    
    
    console({**locals(), **globals()})

def chooseFolder():
    folders = [x for x in os.listdir() if x[:6].isdigit() and os.path.isdir(x)]
    folders = sorted(folders)
    print('=' * 16)
    print('\n'.join(folders))
    print('=' * 16)
    folder = None
    while folder not in folders:
        folder = inputChin('Type folder name (or up down arrow keys too): ', '', history = folders)
    return folder

def chooseDurationOfInterest(folder):
    files = sorted([x for x in os.listdir(folder) if x.endswith('.jpg')])
    print('Total jpg files:', len(files))
    boundaries = []
    for i, prompt in [(0, 'start = '), (-1, 'end = ')]:
        dt = datetime.fromtimestamp(parseFilename(files[i]))
        default = dt.__repr__().split('.', 1)[1]
        boundaries.append(eval(inputChin(prompt, default)).timestamp())
    start, end = boundaries
    
    last_timestamp, time_delta = None, None
    before_start = 0
    duration = []
    for file in files:
        now_timestamp = parseFilename(file)
        if now_timestamp < start:
            before_start += 1
            continue
        if now_timestamp > end:
            break
        if last_timestamp is None:
            last_timestamp = now_timestamp
        else:
            if time_delta is None:
                time_delta = int(inputChin(
                    'time_delta = ', now_timestamp - last_timestamp
                ))
            if abs((now_timestamp - last_timestamp) / time_delta - 1) > TIME_FLUCT_TOLERANCE:
                print('Error! Missing a frame at', datetime.fromtimestamp(last_timestamp + time_delta))
                console(locals())
                exit()
            last_timestamp = now_timestamp
        duration.append(file)
    taken = len(duration)
    print(before_start, 'before start,', taken, 'taken, and', len(files) - before_start - taken, 'after end. ')
    return duration

def chooseRegionOfInterest(folder, duration_of_interest):
    os.chdir(folder)
    image = Image.open(duration_of_interest[-1])
    x1, y1 = 0, 0
    x2, y2 = image.size
    while True:
        try:
            x1, y1, x2, y2 = eval(inputChin('x, y, width, height = ', str((x1, y1, x2, y2))))
        except EOFError as e:
            raise e
        except Exception as e:
            print(e)
            continue
        image = Image.open(duration_of_interest[-1])
        draw = ImageDraw.Draw(image)
        draw.rectangle((x1, y1, x2, y2), outline = 'red')
        del draw
        print('The cropping preview has been shown in red rectangle.')
        print('Close the image window to proceed.')
        image.show()
        print('Are you happy with', (x1, y1, x2, y2), '?', end = ' ')
        if input('y/n > ').lower() == 'y':
            break
    os.chdir('..')
    return x1, y1, x2, y2

def getListOfFrames(folder, duration_of_interest, region_of_interest):
    os.chdir(folder)
    frames = []
    jdt = Jdt(len(duration_of_interest), 'reading', UPP = 8)
    for filename in duration_of_interest:
        jdt.acc()
        try:
            image = Image.open(filename)
        except:
            print('Warning: Failed to open file', filename)
            continue
        frames.append(np.array(image.crop(region_of_interest)))
    jdt.complete()
    os.chdir('..')
    return frames

def parseFilename(filename):
    return int(datetime(*[
        int(filename[x:y]) for x, y in (
            (4, 8), (8, 10), (10, 12), (13, 15), (15, 17), (17, 19), 
        )
    ]).timestamp())

def present(f):
    print('Prepareing to present...')
    mag = np.absolute(f)
    # mag = mag[1:]   # get rid of DC
    n_bins, w, h, n_colors = mag.shape  # this line helps me think
    max_value = np.max(mag)
    while True:
        try:
            stacking_method = eval('np.' + inputChin('stacking_method = ', 'vstack'))
            break
        except EOFError as e:
            raise e
        except Exception as e:
            print(e)
    print('stacking...')
    wide_array = (stacking_method(mag) / max_value * 256).astype(np.uint8)
    wide_image = Image.fromarray(wide_array)
    wide_image.show()
    return locals()

main()

'''
190716_retrieve     (340, 1200, 1750, 2500)
'''

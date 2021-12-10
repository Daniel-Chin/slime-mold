print('loading...')
import cv2
from os import listdir
from numpy import mean
from jdt import Jdt
# from IPython import embed
'''
Test showed: mean(Canny(img, 100, 150)) either < 3 or > 15. 
We will use 9 as threshold. 
... 2019/1/23: For a diff dataset, it's diff. 
'''
THRESHOLD = .1      # Change this value, if we have too many "blurred"
# THRESHOLD is the threshold for blurness of img. For different lighting, placement of dish, or photo sizes, this needs to be re-calibrated. 
RAW = "E:/201127"    # Change this to the folder name
assert input(f'Are we looking at {RAW}? y/n > ') == 'y'
SKIP = 1            # skip frame
print(f'Taking 1 frame per {SKIP} frames')

list_filename = listdir(RAW)
list_filename.sort()
jdt = Jdt(len(list_filename), 'Slime', UPP = 8)
sample = cv2.imread(RAW + '/' + list_filename[0])
resolution = tuple(reversed(sample.shape[:2]))
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, resolution, True)
lastClear = None
i = -1
for filename in list_filename:
    jdt.acc()
    i = (i + 1) % SKIP
    if i != 0:
        continue
    raw = cv2.imread(RAW + '/' + filename)
    # canny = cv2.Canny(raw, 100, 150)
    # blur = mean(canny)
    # if blur < THRESHOLD:
        # if lastClear is None:
            # print('Skipping first blurred frame:', filename)
            # continue
        # cv2.rectangle(lastClear,(0,0),(64,64),(255,255,0),-1)
        # out.write(lastClear)
        # print('\nblur level', blur, ':', filename)
    # else:
        # lastClear = raw
        # out.write(raw)
    out.write(raw)
jdt.complete()
out.release()
cv2.destroyAllWindows()

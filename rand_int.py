from random import randrange

def randInterval(min = 25, max = 40, h_length = 8):
    length = h_length * 60
    intervals = []
    while sum(intervals) < length:
        intervals.append(randrange(min, max + 1))
    if sum(intervals) > length:
        intervals[-1] -= sum(intervals) - length
    return intervals

def printInterval(intervals):
	acc = 0
	on = 1
	sym = ('x', 'O')
	for interval in intervals:
		print('t =', acc, end = '\t')
		acc += interval
		print(format(interval, '2'), sym[on])
		on = 1 - on
	print('t =', acc)

def merge(a, b):
	a = interval2time(a)
	b = interval2time(b)
	last = 0
	status = {'A': 0, 'B': 0}
	verb = ['on', 'off']
	def _pop(a, b):
		if a == []:
			return 'B', b.pop(0)
		if b == []:
			return 'A', a.pop(0)
		if a[0] < b[0]:
			return 'A', a.pop(0)
		else:
			return 'B', b.pop(0)
	while a or b:
		who, value = _pop(a, b)
		print('delay', value - last)
		print('t =', value, '.', 'Turn', verb[status[who]], who)
		status[who] = not status[who]
		last = value

def interval2time(intervals):
	times = [0]
	time = 0
	for interval in intervals:
		time += interval
		times.append(time)
	return times

if __name__ == '__main__':
    help(randInterval)
    code = 'randInterval('
    print(code, end = '', flush = True)
    code += input()
    printInterval(eval(code))
    input('Enter...')

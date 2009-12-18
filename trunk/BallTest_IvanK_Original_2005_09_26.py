from __future__ import division

# make program faster
try:
	import psyco
	psyco.full()
except:
	pass

# testWorldBalls needs to be at least 3000 so that there are enough identical integers in the 5%th location while calculating the "effective minimum"
testWorldBalls = 6000 # MUST BE EVEN NUMBER
testWorldDivisor = int(testWorldBalls/300) # or set to your own number
confidence = 0.95 # confidence for determining the "effective minimum" number of balls with a given pool
runSimTimes = 6000 # higher is better accuracy

import sys

if len(sys.argv) != 3:
	print """
# USAGE: ballcount.py <n, stop at n*poolsize, default 25> <pareto factor, 0 for 1:1, 3.21 for 10:1, and 10.5 for 100:1>
# See http://en.wikipedia.org/wiki/Image:Pareto_distributionPDF.png (this program uses k=1)
# USAGE (for Pareto test): ballcount.py paretotest <pareto factor>
"""

factor = float(sys.argv[2])

import random

def pickPareto(maxNum):
	while True:
		parNum = random.paretovariate(1)-1
		if parNum <= factor-1:
			break
	n = int((parNum/(factor-1))*testWorldBalls)+1
	return n

if sys.argv[1] == "paretotest":
	st = []
	for _ in xrange(6000000):
		st.append(str(pickPareto(testWorldBalls)))
	st = '\n'.join(st)
	for i in xrange(1,testWorldBalls+1):
		print str(i) + ',' + str(st.count('\n'+str(i)+'\n'))
	sys.exit()

def runOnce(numPoolSize):
	"""This determines how many special balls we got - just one attempt."""
	resList = []

	if factor == 0:
		"Factor is 0, using evenly distributed randint"
		for i in xrange(numPoolSize):
			r = random.randint(1,testWorldBalls)
			if r % testWorldDivisor == 0:
				resList.append(r)
	else:
		"Factor is %s, using Pareto k=1 distribution"
		for i in xrange(numPoolSize):
			r = pickPareto(testWorldBalls)
			if r % testWorldDivisor == 0:
				resList.append(r)

	return len(set(resList))

def simulation(numPoolSize):
	# fetchedList is a runSimTimes-length list of the number of special balls you get
	fetchedList = sorted([runOnce(numPoolSize) for t in xrange(runSimTimes)])
	avg = sum(fetchedList)/len(fetchedList) # average
	mi = min(fetchedList)
	ma = max(fetchedList)
	medianPosition = int((0.5)*len(fetchedList))
	median = fetchedList[medianPosition]
	balls300 = fetchedList.count(300)
	# when fetchedList has 4000 elements, getting the element at the 5%th position is [200] of
	# the sorted fetchedList - this effectively eliminates 95% of the best cases, leaving the maximum of the 5% region
	percent5Position = int((1-confidence)*len(fetchedList))
	effectiveMin = fetchedList[percent5Position]
	return "for %s*pool got avg %s, median %s (50%% conf), effective min %s (95%% conf), math min %s max %s avg %s, got %s 300-ball-set (%s%%)" % (numPoolSize/testWorldBalls, avg, median, effectiveMin, mi, ma, avg, balls300, (balls300*100)/len(fetchedList))
	
def runTest():
	for numPoolSize in range(testWorldBalls,testWorldBalls*int(sys.argv[1]),int(testWorldBalls/2)):
		print simulation(numPoolSize)

if __name__ == '__main__':
	runTest()
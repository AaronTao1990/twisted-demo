from twisted.internet import reactor
import random

'''
this is a demo for twisted reactor
'''

def countdown(count, index):
    print 'thread : %d, count : %d..' % (index, count)
    count -= 1
    if count > 0:
        seconds = random.randint(1,3)
        reactor.callLater(seconds, countdown, count, index)

for i in range(5):
    reactor.callWhenRunning(countdown, 5, i)

reactor.run()

from twisted.internet import reactor, defer
import treq

a = treq.get('http://github.com').addCallback(yo)

def yo(d):
	print d

reactor.run()





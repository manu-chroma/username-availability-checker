import treq
from klein import Klein
from twisted.internet.defer import inlineCallbacks, returnValue
 
app = Klein()
 
 
@app.route('/square/submit', methods = ['POST'])
@inlineCallbacks
def square_submit(request):
   x = int(request.args.get('x', [0])[0])
 
   ## simulate calling out to some Web service:
   ##
   r = yield treq.get('http://www.tavendo.com/')
   content = yield r.content()
   y = len(content)
 
   res = x * x + y
   returnValue("{} squared plus {} is {}".format(x, y, res))
 
 
if __name__ == "__main__":
	app.run('localhost', 8080)
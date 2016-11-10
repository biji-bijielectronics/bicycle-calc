# set async_mode to 'threading', 'eventlet', 'gevent' or 'gevent_uwsgi' to
# force a mode else, the best mode is selected automatically from what's
# installed
async_mode = 'gevent'

import time
from flask import Flask, render_template
#import socketio
from flask_socketio import SocketIO

import redis
#sio = socketio.Server(logger=True, async_mode=async_mode)

app = Flask(__name__)
#app.wsgi_app = socketio.Middleware(sio, app.wsgi_app)
app.config['SECRET_KEY'] = 'a34db408c9c0efd21fc0dd1a0901a9e8'
app.config['DEBUG'] = True

sio = SocketIO(app)

thread = None
r = redis.Redis()

pubsub = r.pubsub()
pubsub.subscribe(['adc'])


    

def background_thread():
    """Example of how to send server generated events to clients."""
    while True:
        count = 0

        item = pubsub.get_message()
        if item is not None:
            try:
                msg = str(item['data'])
                print "sending: " + msg
                sio.emit('newData', eval(msg),
                        namespace='/adc')
            except:
                e = sys.exc_info()[0]

                print "something messed up", e

        sio.sleep(0.01)            


@app.route('/')
def index():
    global thread
    if thread is None:
        thread = sio.start_background_task(background_thread)
    return render_template('index.html')





if __name__ == '__main__':
    sio.run(app,host='0.0.0.0', port=8080)

    # if sio.async_mode == 'threading':
    #     # deploy with Werkzeug
    #     app.run(threaded=True)
    # elif sio.async_mode == 'eventlet':
    #     # deploy with eventlet
    #     import eventlet
    #     import eventlet.wsgi
    #     eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
    # elif sio.async_mode == 'gevent':
        # deploy with gevent
        # from gevent import pywsgi
        # try:
        #     from geventwebsocket.handler import WebSocketHandler
        #     websocket = True
        # except ImportError:
        #     websocket = False
        # if websocket:
        #     pywsgi.WSGIServer(('', 8080), app,
        #                       handler_class=WebSocketHandler).serve_forever()
        # else:
        #     pywsgi.WSGIServer(('', 8080), app).serve_forever()
    # elif sio.async_mode == 'gevent_uwsgi':
    #     print('Start the application through the uwsgi server. Example:')
    #     print('uwsgi --http :5000 --gevent 1000 --http-websockets --master '
    #           '--wsgi-file app.py --callable app')
    # else:
    #     print('Unknown async_mode: ' + sio.async_mode)
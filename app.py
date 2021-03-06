#!/usr/bin/env python
import os
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect



RABBITMQ_USER = os.environ.get('RABBITMQ_USER', 'guest')
RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD', RABBITMQ_USER)
RABBITMQ_VHOST = os.environ.get('RABBITMQ_VHOST', '/')
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'localhost')
RABBITMQ_PORT = os.environ.get('RABBITMQ_PORT', '5672')

RABBITMQ_URL = 'amqp://{0}:{1}@{2}:{3}{4}'.format(RABBITMQ_USER, RABBITMQ_PASSWORD,
                                            RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_VHOST)


NAMESPACE = '/test'

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.

from gevent import monkey; 
monkey.patch_socket()

async_mode = "gevent"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode, message_queue=RABBITMQ_URL)
thread = None


def background_thread():
    """Example of how to send server generated events to clients."""
#    count = 0
#    while True:
#        socketio.sleep(10)
#        count += 1
#        socketio.emit('my_response',
#                      {'data': 'Is there anybody out there?', 'count': count},
#                      namespace=NAMESPACE)


@app.route('/')
@app.route('/<room_id>')
def index(room_id='Public'):
    return render_template('index.html', async_mode=socketio.async_mode, room_id=room_id)

@socketio.on('my_event', namespace=NAMESPACE)
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count'], 'speak': True})


@socketio.on('my_broadcast_event', namespace=NAMESPACE)
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count'], 'speak': True},
         broadcast=True)


@socketio.on('join', namespace=NAMESPACE)
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {
            #'data': 'Joined ' + message['room']+ '. In rooms: ' + ', '.join(rooms()),
            'data': 'Joined room ' + message['room'],
            'count': session['receive_count']
        })


@socketio.on('leave', namespace=NAMESPACE)
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {
            #'data': 'Left ' + message['room'] + '. In rooms: ' + ', '.join(rooms()),
            'data': 'Left room ' + message['room'],
            'count': session['receive_count']
        })


@socketio.on('close_room', namespace=NAMESPACE)
def close(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response', {'data': 'Room ' + message['room'] + ' is now closed.',
                         'count': session['receive_count']},
         room=message['room'])
    close_room(message['room'])


@socketio.on('my_room_event', namespace=NAMESPACE)
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count'], 'speak': True},
         room=message['room'])


@socketio.on('disconnect_request', namespace=NAMESPACE)
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()


@socketio.on('my_ping', namespace=NAMESPACE)
def ping_pong():
    emit('my_pong')


@socketio.on('connect', namespace=NAMESPACE)
def test_connect():
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=background_thread)
    emit('my_response', {'data': 'Connected from server!', 'count': 0})


@socketio.on('disconnect', namespace=NAMESPACE)
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app, debug=True)
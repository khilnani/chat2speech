## chat2speech

A chat app that reads aloud chat messages so you do not need to constantly read the chat message log.

Built using the Python Flask and Flask Socket IO libraries, Rabbit MQ and Google's Materialize CSS

Included links to referenced articles and documentation below. Thanks!

![Demo Anim](https://github.com/khilnani/chat2speech/blob/master/images/demo.gif?raw=true "Demo Anim")

## Usage

- Run `docker-compose up`
- Navigate to:
  - http://127.0.0.1:8888/ - Public room
  - http://127.0.0.1:8888/ANY_ROOM_NAME - A room with the name ANY_ROOM_NAM

## Links

Text 2 Speech

- https://developers.google.com/web/updates/2014/01/Web-apps-that-talk-Introduction-to-the-Speech-Synthesis-API
- http://khaidoan.wikidot.com/html5-tts
- https://codepen.io/SteveJRobertson/pen/emGWaR
- https://codepen.io/matt-west/pen/wGzuJ

Flask

- http://flask.pocoo.org/
- https://flask-socketio.readthedocs.io/en/latest/
- https://code.tutsplus.com/tutorials/build-a-real-time-chat-application-with-modulus-and-python--cms-24462

Google Materialize CSS

- http://materializecss.com/

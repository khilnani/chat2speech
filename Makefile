PROJECT_NAME = chat2speech

clean:
	find . -name "*.pyc" -exec rm -rf {} \;

init:
	virtualenv -p `which python2.7` $(WORKON_HOME)/chat2speech
	$(WORKON_HOME)/chat2speech/bin/pip install -U pip wheel
	$(WORKON_HOME)/chat2speech/bin/pip install -Ur requirements.txt
	$(WORKON_HOME)/chat2speech/bin/pip freeze
	@echo ""
	@echo "workon chat2speech"
	@echo "docker-compose up"
	@echo "make run"
	@echo ""

reset:
	rm -rf $(WORKON_HOME)/chat2speech

r:
	pip install -U -r requirements.txt

run:
	# ENV=development, production
	# PORT=8080
	FLASK_APP=app.py FLASK_DEBUG=1 flask run --host=0.0.0.0 --port=$(PORT)
	#FLASK_DEBUG=1 python app.py --host=0.0.0.0 --port=$(PORT)

start:
	# ENV=development, production
	# PORT=8080
	# uwsgi --ini uwsgi.ini:production -H $(WORKON_HOME)/chat2speech
	uwsgi --ini uwsgi.ini:production

stop:
	uwsgi --stop uwsgi.pid

PROJECT_NAME = chat2speech

clean:
	find . -name "*.pyc" -exec rm -rf {} \;

init:
	virtualenv -p `which python2.7` $(WORKON_HOME)/chat2speech
	$(WORKON_HOME)/chat2speech/bin/pip install -U pip wheel
	$(WORKON_HOME)/chat2speech/bin/pip install -Ur requirements/development.txt
	$(WORKON_HOME)/chat2speech/bin/pip freeze
	@echo ""
	@echo "workon chat2speech"
	@echo "docker-compose up"
	@echo "make run"
	@echo ""

reset:
	rm -rf $(WORKON_HOME)/chat2speech

r:
	$(WORKON_HOME)/chat2speech/bin/pip install -U -r requirements/development.txt

run:
	# ENV=development, production
	# PORT=8080
	python app.py

SHELL := bash

run:
	cd modules && docker-compose up --build -d
	
clean:
	cd modules && docker-compose down

logs:
	cd modules && docker-compose logs -f --tail 100

pipenv:
	pipenv install -r requirements.txt

test: 
	cd modules && pipenv run pytest -sv

prepare:
	sudo apt install -y pipenv

all: prepare pipenv run test


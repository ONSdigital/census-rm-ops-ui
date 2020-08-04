build:
	pipenv install --dev

lint:
	pipenv run flake8 ./app
	PIPENV_PYUP_API_KEY="" pipenv check ./app

test: lint
	pipenv run pytest --cov-report term-missing --cov app --capture no

start:
	pipenv run python run.py

docker: test
	docker build -t eu.gcr.io/census-rm-ci/rm/census-rm-ops-ui .

docker-run: docker
	docker run --network=censusrmdockerdev_default  -p 8003:80 eu.gcr.io/census-rm-ci/rm/census-rm-ops-ui:latest

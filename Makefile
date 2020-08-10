build:
	pipenv install --dev

lint:
	pipenv run flake8
	PIPENV_PYUP_API_KEY="" pipenv check

start:
	pipenv run python run.py

docker:
	docker build -t eu.gcr.io/census-rm-ci/rm/census-rm-ops-ui .

docker-run: docker
	docker run --network=censusrmdockerdev_default  -p 8234:8234 eu.gcr.io/census-rm-ci/rm/census-rm-ops-ui:latest

dev:
	pipenv run python -m app

install:
	pipenv install

test:
	pipenv run pytest -vvv -n auto --dist load

build:
	docker build \
		--tag docker.aa12.ml/moretech/api:$V \
		--tag docker.aa12.ml/moretech/api:latest \
		--file templates/Dockerfile \
		.

	docker image push docker.aa12.ml/moretech/api:$V
	docker image push docker.aa12.ml/moretech/api:latest

docker-run:
	docker build \
		--tag moretech/api
		--file templates/Dockerfile \
		.

	docker run -d moretech/api


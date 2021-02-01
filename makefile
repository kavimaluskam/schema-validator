TAG = "schema-validator"

INPUT_PATH = "data/sample.json"
SCHEMA_PATH = "data/schema.json"


build:
	docker build -t $(TAG) .

test:
	docker run --rm $(TAG) pytest

help:
	docker run --rm $(TAG) python cli.py

generate-schema:
	docker run --rm \
		-v `pwd`/data:/app/data \
		$(TAG) \
		python cli.py generate-schema \
		--input_path $(INPUT_PATH)

validate:
	docker run --rm \
		-v `pwd`/data:/app/data \
		$(TAG) \
		python cli.py validate \
		--input_path $(INPUT_PATH) \
		--schema_path $(SCHEMA_PATH)

summary:
	docker run --rm \
		-v `pwd`/data:/app/data \
		$(TAG) \
		python cli.py summary \
		--input_path $(INPUT_PATH)
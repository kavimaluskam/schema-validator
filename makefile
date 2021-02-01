TAG = "schema-validator"

INPUT_PATH = "data/sample-2.json"
SCHEMA_PATH = "data/schema-test-1.json"


build:
	docker build -t $(TAG) .

test:
	docker run --rm $(TAG) pytest

help:
	docker run --rm $(TAG) python cli.py

generate-schema:
	docker run --rm \
		-v data:/app/data \
		$(TAG) \
		python cli.py generate-schema \
		--input_path $(INPUT_PATH)

validate:
	docker run --rm \
		-v data:/app/data \
		$(TAG) \
		python cli.py validate \
		--input_path $(INPUT_PATH) \
		--schema_path $(SCHEMA_PATH)

summary:
	docker run --rm \
		-v data:/app/data \
		$(TAG) \
		python cli.py summary \
		--input_path $(INPUT_PATH)
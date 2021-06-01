.PHONY: fmt
fmt:
	isort . \
	&& black .

.PHONY: lint
lint:
	black --check .
	isort --check .
	flake8 .
	mypy .

.PHONY: test
test:
	pytest --verbose

.PHONY: install
install:
	pip install .

.PHONY: install-dev
install-dev:
	pip install -r requirements.txt \
	&& pip install -e .

.PHONY: readme
readme:
	ffs --help | p2c --tgt _main README.md \
	&& ffs export --help | p2c --tgt _export README.md \
	&& ffs book --help | p2c --tgt _book README.md \
	&& ffs problems --help | p2c --tgt _problems README.md

.PHONY: clean-docs
clean-docs:
	rm -rf docs

.PHONY: docs
docs: clean-docs readme
	mkdir -p docs \
	&& pdoc --html --output-dir docs ffs

.PHONY: update-spec
update-spec:
	cd data-policy \
	&& git pull \
	&& cd .. \
	&& rm -f ffs/{FILE_STRUCTURE,GUIDELINES}.md \
	&& cp data-policy/{FILE_STRUCTURE,GUIDELINES}.md ffs/

.PHONY: clean-book
clean-book:
	rm -rf book/*

book: clean-book
	mkdir -p book \
	&& ffs book data-policy/example book \
	&& mdbook build book

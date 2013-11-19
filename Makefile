test: pytest
	PYTHONPATH=. py.test

pytest:
	@which py.test || $(MAKE) dependencies

dependencies:
	@pip install pytest mock

install:
	pip install -e . --user

upload:
	make clean
	python setup.py sdist bdist_wheel && twine upload dist/*

test:
	pytest

clean:
	python setup.py clean --all
	rm -f *.hdf5 *.yml *.csv
	find . -name "*.pyc" -exec rm -rf {} \;
	find . -type d -name "__pycache__" -delete
	rm -rf build
	rm -rf cover
	rm -rf dist
	rm -rf hwrt.egg-info
	rm -rf tests/reports

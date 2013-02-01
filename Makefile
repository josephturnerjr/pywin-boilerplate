
BASENAME = Example

PROJECTVERSION = "internal"

all: project

resources: 
	python build_resources.py

project: resources
	echo "version = \"$(PROJECTVERSION)\"" > VERSION.py
	python -O -O setup.py py2exe

clean:
	rm -rf dist build *.pyc log.txt

.PHONY: resources package

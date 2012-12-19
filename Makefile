PY_VER  = $(shell python -V 2>&1 | cut -f 2 -d ' ' | cut -f 1 -d .)

ifeq ($(PY_VER), 3)
    PYTHON=python2
else
    PYTHON=python

endif

run: bin/py

bin/py: bin/buildout buildout.cfg

bin/buildout: bootstrap.py
	$(PYTHON) bootstrap.py
	bin/buildout

bootstrap.py:
	wget http://python-distribute.org/bootstrap.py
	
test: bin/py
	bin/test
	
dev: bin/buildout dev.cfg
	bin/buildout -c dev.cfg
	


PROJECT = plots
MAIN = $(PROJECT).py
PYTHON = python
PYLINT = pylint
TEST_PATH = tests
PROF_CTD = netcdf/OS_PIRATA-FR31_CTD.nc -t CTD -p -k PRES TEMP PSAL DOX2 FLU2 -g -c k- b- r- m- g- -g -l 5 9
SECT_CTD = netcdf/OS_PIRATA-FR31_CTD.nc -t CTD -s -k PRES TEMP -a LATITUDE -l 5 22
PROF_XBT = netcdf/OS_PIRATA-FR31_XBT.nc -t XBT -p -k DEPTH TEMP DENS SVEL -c k- b- k- g- -g -l 1 5
PROF_ADCP = netcdf/OS_PIRATA-FR31_ADCP.nc -t ADCP -p -k DEPTH EWCT NSCT -c k- r- b- -g -l 5 22
SECT_XBT = netcdf/OS_PIRATA-FR31_XBT.nc -t XBT -s DEPTH TEMP -a LATITUDE -l 5 10

.PHONY: clean-pyc clean-build lint test run build

clean-all:  clean-pyc clean-build

clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	
clean-build:
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive __pycache__/

lint:
	$(PYLINT) --exclude=.tox

test: 
	$(PYTHON) -m unittest  discover -v  $(TEST_PATH)

ctdp:
	$(PYTHON) $(MAIN) $(PROF_CTD)

ctds:
	$(PYTHON) $(MAIN) $(SECT_CTD)

xbtp:
	$(PYTHON) $(MAIN) $(PROF_XBT)

xbts:
	$(PYTHON) $(MAIN) $(SECT_XBT)

adcp:
	$(PYTHON) $(MAIN) $(PROF_LADCP)

build:
	pyinstaller -wF --clean $(MAIN)

runc:
	dist/$(PROJECT)

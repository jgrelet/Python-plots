PROJECT = plots
MAIN = $(PROJECT).py
PYTHON = python
PYLINT = pylint
TEST_PATH = tests
PROF_CTD = netcdf/OS_PIRATA-FR31_CTD.nc -t CTD -p -k PRES TEMP PSAL DOX2 FLU2 -g -c k- b- r- m- g- -g -l 5 9
SECT_CTD = netcdf/OS_PIRATA-FR31_CTD.nc -t CTD -s -k PRES TEMP --xaxis LATITUDE -l 5 22 --yscale 0 250 250 2000 --xinterp 24 --yinterp 200 --clevels=30 --autoscale 0 30
PROF_ADCP = netcdf/OS_PIRATA-FR31_ADCP.nc -t ADCP -p -k DEPTH EWCT NSCT -c k- r- b- -g -l 28 32
SECT_ADCP = netcdf/OS_PIRATA-FR31_ADCP.nc -t ADCP -s -k DEPTH EWCT NSCT -l 28 32 -l 33 45 --xaxis TIME --yscale 0 500 --xinterp 20 --yinterp 50 --clevels 15 --autoscale -150 150
PROF_XBT = netcdf/OS_PIRATA-FR31_XBT.nc -t XBT -p -k DEPTH TEMP DENS SVEL -c k- b- k- g- -g -l 1 5
SECT_XBT = netcdf/OS_PIRATA-FR31_XBT.nc -t XBT -s -k DEPTH TEMP --xaxis TIME -l 29 36

.PHONY: clean-pyc clean-build clean lint test run build

clean-all:  clean-pyc clean-build clean

clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	
clean-build:
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive __pycache__/

clean:
	ls plots/*
	rm sections/*

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

adcpp:
	$(PYTHON) $(MAIN) $(PROF_ADCP)

adcps:
	$(PYTHON) $(MAIN) $(SECT_ADCP)

build:
	pyinstaller -wF --clean $(MAIN)

runc:
	dist/$(PROJECT)

PROJECT = plots
MAIN = $(PROJECT).py
PYTHON = python
PYLINT = pylint
TEST_PATH = tests
PROF_CTD = netcdf/OS_PIRATA-FR31_CTD.nc -t CTD -p -k PRES TEMP PSAL DOX2 FLU2 -g -c k- b- r- m- g- -g -l 1 5
SECT_CTD = netcdf/OS_PIRATA-FR31_CTD.nc -t CTD -s --append 1N-10W_10S_10W -k PRES TEMP --xaxis LATITUDE -l 5 28 --yscale 0 250 250 2000 --xinterp 24 --yinterp 200 --clevels=30 --autoscale 0 30
SECT2_CTD = netcdf/OS_PIRATA-FR31_CTD.nc -t CTD -s --append point-fixe_0-10W -k PRES TEMP --xaxis TIME -l 33 49 --yscale 0 200 --xinterp 17 --yinterp 20 --clevels=30 --autoscale 0 30
SECT3_CTD = netcdf/OS_PIRATA-FR31_CTD.nc -t CTD -s --append point-fixe_0-23W -k PRES TEMP --xaxis TIME -l 54 61 --yscale 0 200 --xinterp 17 --yinterp 20 --clevels=30 --autoscale 0 30
PROF_ADCP = netcdf/OS_PIRATA-FR31_ADCP.nc -t ADCP -p -k DEPTH EWCT NSCT -c k- r- b- -g -l 28 32
SECT_ADCP = netcdf/OS_PIRATA-FR31_ADCP.nc -t ADCP -s --append 1N-10W_10S_10W -k DEPTH EWCT NSCT -l 5 28 --xaxis LATITUDE --yscale 0 250 250 2000 --xinterp 24 --yinterp 100 --clevels 30 --autoscale -150 150
PROF_XBT = netcdf/OS_PIRATA-FR31_XBT.nc -t XBT -p -k DEPTH TEMP DENS SVEL -c k- b- k- g- -g -l 1 5
SECT_XBT = netcdf/OS_PIRATA-FR31_XBT.nc -t XBT -s --append 10S-20S_10W -k DEPTH TEMP --xaxis LATITUDE -l 18 28 --yscale 0 250 250 900
SECT2_XBT = netcdf/OS_PIRATA-FR31_XBT.nc -t XBT -s --append 0-10W_0_23W -k DEPTH TEMP --xaxis LONGITUDE -l 39 61 --yscale 0 250 250 900 --xinterp 20 --yinterp 200 --clevels 30 -e  59

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
	rm plots/*
	rm sections/*

lint:
	$(PYLINT) --exclude=.tox

test: 
	$(PYTHON) -m unittest  discover -v  $(TEST_PATH)

ctdp:
	$(PYTHON) $(MAIN) $(PROF_CTD)

ctds:
	$(PYTHON) $(MAIN) $(SECT_CTD)

ctd2s:
	$(PYTHON) $(MAIN) $(SECT2_CTD)

ctd3s:
	$(PYTHON) $(MAIN) $(SECT3_CTD)

xbtp:
	$(PYTHON) $(MAIN) $(PROF_XBT)

xbts:
	$(PYTHON) $(MAIN) $(SECT_XBT)

xbt2s:
	$(PYTHON) $(MAIN) $(SECT2_XBT)

adcpp:
	$(PYTHON) $(MAIN) $(PROF_ADCP)

adcps:
	$(PYTHON) $(MAIN) $(SECT_ADCP)

build:
	pyinstaller -wF --clean $(MAIN)

runc:
	dist/$(PROJECT)

PROJECT = plots
MAIN = $(PROJECT).py
PYTHON ?= python
TEST_PATH = tests

.PHONY: help clean-pyc clean-build clean test smoke check all \
	ctdp ctds xbtp xbts adcpp adcps tsgs gosud

help:
	@echo "Targets: all check test smoke ctdp ctds xbtp xbts adcpp adcps tsgs gosud clean"

clean-pyc:
	$(PYTHON) -c "from pathlib import Path; [p.unlink(missing_ok=True) for p in Path('.').rglob('*.pyc')]; [p.unlink(missing_ok=True) for p in Path('.').rglob('*.pyo')]"

clean-build:
	$(PYTHON) -c "import shutil; [shutil.rmtree(path, ignore_errors=True) for path in ('build', 'dist', '__pycache__')]"

clean:
	$(PYTHON) -c "import shutil; [shutil.rmtree(path, ignore_errors=True) for path in ('plots/profiles', 'plots/sections', 'plots/scatters', 'plots/tmp-smoke', 'sections', 'scatters')]"

test:
	$(PYTHON) -m unittest discover -s $(TEST_PATH) -v

smoke:
	$(PYTHON) -m unittest tests.test_smoke -v

check:
	$(PYTHON) -m compileall $(MAIN)
	$(MAKE) test

all: ctdp ctds xbtp xbts adcpp adcps tsgs gosud

ctdp:
	$(PYTHON) $(MAIN) netcdf/OS_AMAZOMIX_CTD.nc -t CTD -p -k PRES TEMP PSAL DOX2 FLU2 -g -c k- b- r- m- g- -o plots/AMAZOMIX

ctds:
	$(PYTHON) $(MAIN) netcdf/OS_PIRATA-FR31_CTD.nc -t CTD -s --append 1N-10W_10S_10W -k PRES TEMP --xaxis LATITUDE -l 5 28 --yscale 0 250 250 2000 --xinterp 24 --yinterp 10 --clevels 30 --autoscale 0 30 -o plots/sections/PIRATA-FR31

xbtp:
	$(PYTHON) $(MAIN) netcdf/OS_PIRATA-FR31_XBT.nc -t XBT --profiles -k DEPTH TEMP DENS SVEL -c k- b- k- g- -g -l 1 5 -o plots/PIRATA-FR31

xbts:
	$(PYTHON) $(MAIN) netcdf/OS_PIRATA-FR31_XBT.nc -t XBT -s --append 10S-20S_10W -k DEPTH TEMP --xaxis LATITUDE -l 18 28 --yscale 0 250 250 900 -o plots/sections/PIRATA-FR31

adcpp:
	$(PYTHON) $(MAIN) netcdf/OS_PIRATA-FR31_ADCP.nc -t ADCP --profile -k DEPTH EWCT NSCT -c k- r- b- -g -l 28 32 -o plots/PIRATA-FR31

adcps:
	$(PYTHON) $(MAIN) netcdf/OS_PIRATA-FR31_ADCP.nc -t ADCP --section --append 1N-10W_10S_10W -k DEPTH EWCT NSCT -l 5 28 --xaxis LATITUDE --yscale 0 250 250 2000 --xinterp 24 --yinterp 20 --clevels 30 --autoscale -150 150 -o plots/sections/PIRATA-FR31

tsgs:
	$(PYTHON) $(MAIN) netcdf/OS_AMAZOMIX_TSG.nc -t TSG --scatter -k SSPS SSTP -o plots/scatters/AMAZOMIX

gosud:
	$(PYTHON) $(MAIN) netcdf/TOUC0702.nc -t TSG --scatter --dims DAYD LATX LONX -k SSPS SSJT -o plots/scatters/GOSUD

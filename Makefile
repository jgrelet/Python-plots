PROJECT = plots
MAIN = ${PROJECT}.py
CRUISE = PIRATA-FR31
PROF_DIR = plots
SECT_DIR = coupes
PYTHON = python
PYLINT = pylint
TEST_PATH = tests
PROF_CTD = netcdf/OS_${CRUISE}_CTD.nc -t CTD -p -k PRES TEMP PSAL DOX2 FLU2 -g \
			-c k- b- r- m- g- -g -l 1 5 -o ${PROF_DIR}
SECT_CTD = netcdf/OS_${CRUISE}_CTD.nc -t CTD -s --append 1N-10W_10S_10W -k PRES TEMP \
			--xaxis LATITUDE -l 5 28 --yscale 0 250 250 2000 --xinterp 24 --yinterp 10 \
			--clevels=30 --autoscale 0 30 -o ${SECT_DIR}
SECT2_CTD = netcdf/OS_${CRUISE}_CTD.nc -t CTD -s --append point-fixe_0-10W -k PRES TEMP \
			--xaxis TIME -l 33 49 --yscale 0 200 --xinterp 17 --yinterp 10 --clevels=30 \
			--autoscale 0 3 -o ${SECT_DIR}
SECT3_CTD = netcdf/OS_${CRUISE}_CTD.nc -t CTD -s --append point-fixe_0-23W -k PRES TEMP \
			--xaxis TIME -l 54 69 --yscale 0 200 --xinterp 17 --yinterp 10 --clevels=30 \
			--autoscale 0 30 -o ${SECT_DIR}
PROF_ADCP = netcdf/OS_${CRUISE}_ADCP.nc -t ADCP -p -k DEPTH EWCT NSCT -c k- r- b- -g \
			-l 28 32 -o ${PROF_DIR}
SECT_ADCP = netcdf/OS_${CRUISE}_ADCP.nc -t ADCP -s --append 1N-10W_10S_10W -k DEPTH EWCT NSCT \
			-l 5 28 --xaxis LATITUDE --yscale 0 250 250 2000 --xinterp 24 --yinterp 20 \
			--clevels 30 --autoscale -150 150 -o ${SECT_DIR}
PROF_XBT = netcdf/OS_${CRUISE}_XBT.nc -t XBT -p -k DEPTH TEMP DENS SVEL -c k- b- k- g- -g \
			-l 1 5 -o ${PROF_DIR}
SECT_XBT = netcdf/OS_${CRUISE}_XBT.nc -t XBT -s --append 10S-20S_10W -k DEPTH TEMP \
			--xaxis LATITUDE -l 18 28 --yscale 0 250 250 900 -o ${SECT_DIR}
SECT2_XBT = netcdf/OS_${CRUISE}_XBT.nc -t XBT -s --append 0-10W_0_23W -k DEPTH TEMP \
			--xaxis LONGITUDE -l 39 61 --yscale 0 250 250 900 --xinterp 20 --yinterp 10 \
			--clevels 30 --autoscale 0 30 -e 59 -o ${SECT_DIR}
SECT3_XBT = netcdf/OS_${CRUISE}_XBT.nc -t XBT -s --append 4N_23W_CANARIES -k DEPTH TEMP \
			--xaxis LATITUDE -l 62 75 --yscale 0 250 250 900  --yinterp 10 \
			--clevels 30 --autoscale 0 30  -o ${SECT_DIR}

.PHONY: clean-pyc clean-build clean lint test run build

clean-all:  clean-pyc clean-build clean

clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	
clean-build:
ifeq ($(OS),Windows_NT) 
		del /Q build dist __pycache__
else
		rm --force --recursive build/
		rm --force --recursive dist/
		rm --force --recursive __pycache__/
endif

clean:
ifeq ($(OS),Windows_NT)
		del /Q $(PROF_DIR)
		del /Q $(SECT_DIR)
else
		rm plots/*
		rm sections/*
endif

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

xbt3s:
	$(PYTHON) $(MAIN) $(SECT3_XBT)

adcpp:
	$(PYTHON) $(MAIN) $(PROF_ADCP)

adcps:
	$(PYTHON) $(MAIN) $(SECT_ADCP)

build:
	pyinstaller -wF --clean $(MAIN)

runc:
	dist/$(PROJECT)

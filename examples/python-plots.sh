#!/bin/bash

shopt -s expand_aliases
export HOME=/home/science
export DRIVE=/mnt/campagnes
export CRUISE=PIRATA-FR31
echo "Trying to source ${DRIVE}/${CRUISE}/local/etc/skel/.bashrc.${CRUISE}"
if [ -f ${DRIVE}/${CRUISE}/local/etc/skel/.bashrc.${CRUISE} ]; then
  . ${DRIVE}/${CRUISE}/local/etc/skel/.bashrc.${CRUISE}
  echo "Yes, seems good !!!"
else
  echo "Can't source file !!! check your network, hard drive and/or ENV variables !!!"
fi

# plot profiles and sections
export NC_DIR=netcdf
export PROF_DIR=plots/python
export SECT_DIR=coupes/python

echo ""
echo "Python plots processing:"
echo "------------------------"

CTD
echo "CTD profiles:"
# all profiles
#plots.py $NC_DIR/OS_${CRUISE}_CTD.nc --type CTD --profiles -k PRES TEMP PSAL DOX2 FLU2 -g -c k- b- r- m- g- -g -o $PROF_DIR
echo "CTD sections:"
# section 10W
plots.py $NC_DIR/OS_${CRUISE}_CTD.nc --type CTD --sections --append 1N-10W_10S-10W -k PRES TEMP --xaxis LATITUDE -l 5 28 --yscale 0 250 250 2000 --yinterp 10 --clevels=30 --autoscale 0 30 -o $SECT_DIR
plots.py $NC_DIR/OS_${CRUISE}_CTD.nc --type CTD --sections --append 1N-10W_10S-10W -k PRES PSAL --xaxis LATITUDE -l 5 28 --yscale 0 250 250 2000 --yinterp 10 --clevels=20 --autoscale 33 37 -o $SECT_DIR
plots.py $NC_DIR/OS_${CRUISE}_CTD.nc --type CTD --sections --append 1N-10W_10S_10W -k PRES DENS --xaxis LATITUDE -l 5 28 --yscale 0 250 250 2000 --yinterp 10 --clevels=20 --autoscale 20 30 -o $SECT_DIR
plots.py $NC_DIR/OS_${CRUISE}_CTD.nc --type CTD --sections --append 1N-10W_10S-10W -k PRES DOX2 --xaxis LATITUDE -l 5 28 --yscale 0 250 250 2000 --yinterp 10 --clevels=20 --autoscale 0 250 -o $SECT_DIR
plots.py $NC_DIR/OS_${CRUISE}_CTD.nc --type CTD --sections --append 1N-10W_10S-10W -k PRES FLU2 --xaxis LATITUDE -l 5 28 --yscale 0 250 --yinterp 10 --clevels 20 --autoscale 0 2 -o $SECT_DIR
# point fixe 0-10W
plots.py $NC_DIR/OS_${CRUISE}_CTD.nc --type CTD --sections --append point-fixe_0-10W -k PRES TEMP --xaxis TIME -l 33 48 --yscale 0 200 --yinterp 10 --clevels=30 --autoscale 0 30 -o $SECT_DIR
plots.py $NC_DIR/OS_${CRUISE}_CTD.nc --type CTD --sections --append point-fixe_0-10W -k PRES PSAL --xaxis TIME -l 33 48 --yscale 0 200 --yinterp 10 --clevels=20 --autoscale 33 37 -o $SECT_DIR
plots.py $NC_DIR/OS_${CRUISE}_CTD.nc --type CTD --sections --append point-fixe_0-10W -k PRES DENS --xaxis TIME -l 33 48 --yscale 0 200 --yinterp 10 --clevels=20 --autoscale 20 30 -o $SECT_DIR
plots.py $NC_DIR/OS_${CRUISE}_CTD.nc --type CTD --sections --append point-fixe_0-10W -k PRES DOX2 --xaxis TIME -l 33 48 --yscale 0 200 --yinterp 10 --clevels=20 --autoscale 0 250 -o $SECT_DIR
plots.py $NC_DIR/OS_${CRUISE}_CTD.nc --type CTD --sections --append point-fixe_0-10W -k PRES FLU2 --xaxis TIME -l 33 48 --yscale 0 200 --yinterp 10 --clevels 20 --autoscale 0 2 -o $SECT_DIR
# section 23W
plots.py $NC_DIR/OS_${CRUISE}_CTD.nc --type CTD --sections --append 2S-4N_23W -k PRES TEMP --xaxis LATITUDE -l 50 78 --yscale 0 250 250 2000 --yinterp 10 --clevels=30 --autoscale 0 30 -o $SECT_DIR --exclude 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69
plots.py $NC_DIR/OS_${CRUISE}_CTD.nc --type CTD --sections --append 2S-4N_23W -k PRES PSAL --xaxis LATITUDE -l 50 78 --yscale 0 250 250 2000 --yinterp 10 --clevels=20 --autoscale 33 37 -o $SECT_DIR --exclude 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69
plots.py $NC_DIR/OS_${CRUISE}_CTD.nc --type CTD --sections --append 2S-4N_23W -k PRES DENS --xaxis LATITUDE -l 50 78 --yscale 0 250 250 2000 --yinterp 10 --clevels=20 --autoscale 20 30 -o $SECT_DIR --exclude 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69
plots.py $NC_DIR/OS_${CRUISE}_CTD.nc --type CTD --sections --append 2S-4N_23W -k PRES DOX2 --xaxis LATITUDE -l 50 78 --yscale 0 250 250 2000 --yinterp 10 --clevels=20 --autoscale 0 250 -o $SECT_DIR --exclude 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69
plots.py $NC_DIR/OS_${CRUISE}_CTD.nc --type CTD --sections --append 2S-4N_23W -k PRES FLU2 --xaxis LATITUDE -l 50 78 --yscale 0 250 --yinterp 10 --clevels 20 --autoscale 0 2 -o $SECT_DIR --exclude 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69
# point fixe 0-23W
plots.py $NC_DIR/OS_${CRUISE}_CTD.nc --type CTD --sections --append point-fixe_0-23W -k PRES TEMP --xaxis TIME -l 54 69 --yscale 0 200 --yinterp 10 --clevels=30 --autoscale 0 30 -o $SECT_DIR
plots.py $NC_DIR/OS_${CRUISE}_CTD.nc --type CTD --sections --append point-fixe_0-23W+profiles -k PRES TEMP --xaxis TIME -l 54 69 --yscale 0 200 --yinterp 10 --clevels=30 --autoscale 0 30 -o $SECT_DIR --display
plots.py $NC_DIR/OS_${CRUISE}_CTD.nc --type CTD --sections --append point-fixe_0-23W -k PRES PSAL --xaxis TIME -l 54 69 --yscale 0 200 --yinterp 10 --clevels=20 --autoscale 33 37 -o $SECT_DIR
plots.py $NC_DIR/OS_${CRUISE}_CTD.nc --type CTD --sections --append point-fixe_0-23W+profiles -k PRES PSAL --xaxis TIME -l 54 69 --yscale 0 200 --yinterp 10 --clevels=20 --autoscale 33 37 -o $SECT_DIR --display
plots.py $NC_DIR/OS_${CRUISE}_CTD.nc --type CTD --sections --append point-fixe_0-23W -k PRES DENS --xaxis TIME -l 54 69 --yscale 0 200 --yinterp 10 --clevels=20 --autoscale 20 30 -o $SECT_DIR
plots.py $NC_DIR/OS_${CRUISE}_CTD.nc --type CTD --sections --append point-fixe_0-23W -k PRES DOX2 --xaxis TIME -l 54 69 --yscale 0 200 --yinterp 10 --clevels=20 --autoscale 0 250 -o $SECT_DIR
plots.py $NC_DIR/OS_${CRUISE}_CTD.nc --type CTD --sections --append point-fixe_0-23W+profiles -k PRES DOX2 --xaxis TIME -l 54 69 --yscale 0 200 --yinterp 10 --clevels=20 --autoscale 0 250 -o $SECT_DIR --display
plots.py $NC_DIR/OS_${CRUISE}_CTD.nc --type CTD --sections --append point-fixe_0-23W -k PRES FLU2 --xaxis TIME -l 54 69 --yscale 0 200 --yinterp 10 --clevels 20 --autoscale 0 2 -o $SECT_DIR

XBT
echo "XBT profiles:"
# all profiles
plots.py $NC_DIR/OS_${CRUISE}_XBT.nc --type XBT --profiles -k DEPTH TEMP DENS SVEL -c k- b- k- g- -g -o plots
echo "XBT sections:"
# sections
plots.py $NC_DIR/OS_${CRUISE}_XBT.nc --type XBT --sections --append CANARIES_1-30N-10W -k DEPTH TEMP --xaxis LATITUDE -l 2 17 --yscale 0 250 250 900 --xinterp 15 --yinterp 10 --clevels=30 --autoscale 0 30 -o $SECT_DIR
plots.py $NC_DIR/OS_${CRUISE}_XBT.nc --type XBT --sections --append 10S-20S_10W -k DEPTH TEMP --xaxis LATITUDE -l 18 28 --yscale 0 250 250 900 --xinterp 10 --yinterp 10 --clevels=30 --autoscale 0 30 -o $SECT_DIR
plots.py $NC_DIR/OS_${CRUISE}_XBT.nc --type XBT --sections --append 10S-10W_0-0 -k DEPTH TEMP --xaxis LATITUDE -l 29 39 --yscale 0 250 250 900 --xinterp 11 --yinterp 10 --clevels=30 --autoscale 0 30 -o $SECT_DIR
plots.py $NC_DIR/OS_${CRUISE}_XBT.nc --type XBT --sections --append 0-10W_0-23W -k DEPTH TEMP --xaxis LONGITUDE -l 39 61 --yscale 0 250 250 900 --xinterp 22 --yinterp 10 --clevels=30 --autoscale 0 30 -o $SECT_DIR -e 59
plots.py $NC_DIR/OS_${CRUISE}_XBT.nc --type XBT --sections --append 4N-23W_CANARIES -k DEPTH TEMP --xaxis LATITUDE -l 62 75 --yscale 0 250 250 900 --yinterp 10 --clevels=30 --autoscale 0 30 -o $SECT_DIR --display

LADCP
echo "LADCP profiles:"
# all profiles
#plots.py $NC_DIR/OS_${CRUISE}_ADCP.nc --type ADCP --profiles -k DEPTH EWCT NSCT -c k- r- b- -g -o $PROF_DIR
echo "LADCP sections:"
# sections
plots.py $NC_DIR/OS_${CRUISE}_ADCP.nc --type ADCP --sections --append 1N-10W_10S-10W -k DEPTH EWCT NSCT -l 5 28 --xaxis LATITUDE --yscale 0 250 250 2000  --yinterp 20 --clevels 30 --autoscale -150 150 -o $SECT_DIR
plots.py $NC_DIR/OS_${CRUISE}_ADCP.nc --type ADCP --sections --append point-fixe_0-10W -k DEPTH EWCT NSCT -l 33 48 --xaxis TIME --yscale 0 500 --yinterp 20 --clevels 30 --autoscale -150 150 -o $SECT_DIR
plots.py $NC_DIR/OS_${CRUISE}_ADCP.nc --type ADCP --sections --append 2S-4N_23W -k DEPTH EWCT NSCT -l 50 78 --xaxis LATITUDE --yscale 0 250 250 2000  --yinterp 20 --clevels 30 --autoscale -150 150 -o $SECT_DIR --exclude 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69
plots.py $NC_DIR/OS_${CRUISE}_ADCP.nc --type ADCP --sections --append point-fixe_0-23W -k DEPTH EWCT NSCT -l 54 69 --xaxis TIME --yscale 0 500  --yinterp 20 --clevels 30 --autoscale -150 150 -o $SECT_DIR
